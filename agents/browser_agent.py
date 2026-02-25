"""
Azure AI Foundry Agent with local MCP server support.
Uses AIProjectClient directly for native Azure AI Foundry tracing.
Bridges MCP tools from Playwright for browser automation.
"""

import os
import json
import asyncio
from typing import Optional
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    FunctionTool,
    ToolSet,
    RequiredFunctionToolCall,
    SubmitToolOutputsAction,
    MessageRole,
    RunStatus,
)
from azure.identity import DefaultAzureCredential
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from configs.settings import Settings
from prompts.gameplay import AI_PLAYER_SYSTEM_PROMPT

settings = Settings()


class BrowserAgentSession:
    """
    Azure AI Foundry Agent session with MCP tool bridging.
    Uses AIProjectClient directly for native tracing support.
    """
    
    def __init__(self):
        self.project_client: Optional[AIProjectClient] = None
        self.mcp_session: Optional[ClientSession] = None
        self.mcp_context = None
        self.agent = None
        self.thread = None
        self.mcp_tools = []
        self._read_stream = None
        self._write_stream = None
    
    async def __aenter__(self):
        # Initialize Azure AI Project client
        credential = DefaultAzureCredential()
        self.project_client = AIProjectClient(
            endpoint=settings.AZURE_AI_PROJECT_ENDPOINT,
            credential=credential,
        )
        
        # Start Playwright MCP server
        server_params = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp", "--browser", "chromium"],
            env={
                **os.environ,
                "DISPLAY": os.environ.get("DISPLAY", ":0"),
                "WAYLAND_DISPLAY": os.environ.get("WAYLAND_DISPLAY", "wayland-0"),
            }
        )
        
        # Connect to MCP server
        self.mcp_context = stdio_client(server_params)
        self._read_stream, self._write_stream = await self.mcp_context.__aenter__()
        self.mcp_session = ClientSession(self._read_stream, self._write_stream)
        await self.mcp_session.__aenter__()
        await self.mcp_session.initialize()
        
        # Get available MCP tools
        tools_result = await self.mcp_session.list_tools()
        self.mcp_tools = tools_result.tools
        
        # Convert MCP tools to Azure function definitions
        function_definitions = self._create_function_definitions()
        
        # Create Azure AI Foundry agent
        self.agent = self.project_client.agents.create_agent(
            model="gpt-4o",
            name="BrowserAgent",
            instructions=AI_PLAYER_SYSTEM_PROMPT,
            tools=function_definitions,
        )
        
        # Create conversation thread
        self.thread = self.project_client.agents.create_thread()
        
        print(f"Agent created: {self.agent.id}")
        print(f"Thread created: {self.thread.id}")
        print(f"MCP tools available: {[t.name for t in self.mcp_tools]}")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup Azure resources
        if self.agent:
            self.project_client.agents.delete_agent(self.agent.id)
            print(f"Agent deleted: {self.agent.id}")
        if self.thread:
            self.project_client.agents.delete_thread(self.thread.id)
        
        # Cleanup MCP session
        if self.mcp_session:
            await self.mcp_session.__aexit__(exc_type, exc_val, exc_tb)
        if self.mcp_context:
            await self.mcp_context.__aexit__(exc_type, exc_val, exc_tb)
    
    def _create_function_definitions(self) -> list:
        """Convert MCP tools to Azure function tool definitions."""
        functions = []
        
        # Add wait tool
        functions.append({
            "type": "function",
            "function": {
                "name": "wait",
                "description": "Pause execution for the specified number of seconds before continuing.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "seconds": {
                            "type": "integer",
                            "description": "Number of seconds to wait (max 60)"
                        }
                    },
                    "required": ["seconds"]
                }
            }
        })
        
        # Convert MCP tools
        for tool in self.mcp_tools:
            func_def = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or f"MCP tool: {tool.name}",
                    "parameters": tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}}
                }
            }
            functions.append(func_def)
        
        return functions
    
    async def _handle_tool_call(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool call and return the result."""
        if tool_name == "wait":
            seconds = min(arguments.get("seconds", 1), 60)
            print(f"wait for {seconds} seconds")
            await asyncio.sleep(seconds)
            return f"Waited {seconds} seconds. Ready to continue."
        
        # Call MCP tool
        try:
            result = await self.mcp_session.call_tool(tool_name, arguments)
            # Extract text content from result
            if result.content:
                return "\n".join(
                    c.text if hasattr(c, 'text') else str(c) 
                    for c in result.content
                )
            return "Tool executed successfully"
        except Exception as e:
            return f"Tool error: {str(e)}"
    
    async def run(self, prompt: str) -> str:
        """Run a prompt and return the response."""
        # Add user message
        self.project_client.agents.create_message(
            thread_id=self.thread.id,
            role=MessageRole.USER,
            content=prompt,
        )
        
        # Create and poll run
        run = self.project_client.agents.create_run(
            thread_id=self.thread.id,
            agent_id=self.agent.id,
        )
        
        # Process until complete
        while run.status in [RunStatus.QUEUED, RunStatus.IN_PROGRESS, RunStatus.REQUIRES_ACTION]:
            await asyncio.sleep(0.5)
            run = self.project_client.agents.get_run(
                thread_id=self.thread.id,
                run_id=run.id,
            )
            
            # Handle tool calls
            if run.status == RunStatus.REQUIRES_ACTION:
                if isinstance(run.required_action, SubmitToolOutputsAction):
                    tool_outputs = []
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        if isinstance(tool_call, RequiredFunctionToolCall):
                            args = json.loads(tool_call.function.arguments)
                            result = await self._handle_tool_call(
                                tool_call.function.name, 
                                args
                            )
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": result,
                            })
                    
                    # Submit tool outputs
                    run = self.project_client.agents.submit_tool_outputs_to_run(
                        thread_id=self.thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs,
                    )
        
        # Get response
        messages = self.project_client.agents.list_messages(thread_id=self.thread.id)
        
        # Return latest assistant message
        for msg in messages.data:
            if msg.role == MessageRole.ASSISTANT:
                if msg.content:
                    return msg.content[0].text.value
        
        return "No response generated"


async def run_browser_agent(prompt: str) -> str:
    """
    Run the browser agent with a single prompt.
    
    Args:
        prompt: The task prompt to send to the agent
        
    Returns:
        The agent's response text
    """
    async with BrowserAgentSession() as session:
        return await session.run(prompt)
