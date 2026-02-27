from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic_ai.agent import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.tools import Tool
from agents.models.azure_openai import azure_model
from pydantic_ai.mcp import MCPServer
from servers.playwright_server import playwright_server
from tools.timer import wait
from prompts.gameplay import AI_PLAYER_SYSTEM_PROMPT


class Status(BaseModel):
    thought: str
    action: str
    observation: str
    browser_close: bool

class BrowserAgent:

    def __init__(
        self, 
        sys_prompt: str, 
        model: OpenAIModel, 
        mcp_servers: Optional[List[MCPServer]] = None, 
        tools: Optional[List[Tool]] = None, 
    ): 
        self.agent = Agent(
            output_type=[Status], 
            model=model, 
            mcp_servers=mcp_servers, 
            system_prompt=sys_prompt,
            tools=tools
        )
        self._mcp_cm = None

    async def __aenter__(self):
        self._mcp_cm = self.agent.run_mcp_servers()
        await self._mcp_cm.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._mcp_cm:
            await self._mcp_cm.__aexit__(exc_type, exc, tb)

    async def run(self, message: str): 
        res = await self.agent.run(message)
        return res.output
        
