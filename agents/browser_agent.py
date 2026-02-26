"""
Assessment Agent - Evaluates security risk using policies and threat intelligence.
"""

import json
import httpx
import os
from typing import Optional
from pydantic import BaseModel, Field
from azure.ai.projects import AIProjectClient
from prompts.gameplay import AI_PLAYER_SYSTEM_PROMPT

class GameStatus(BaseModel):
    """Game Status"""
    thought: str
    action: str
    observation: str
    game_complete: bool

class BrowserAgent:
    """Perform browser action"""
    
    def __init__(
        self,
        client: AIProjectClient,
        model: str = "gpt-4"
    ):
        """
        Initialize Assessment Agent.
        
        Args:
            client: Azure AI Project client
            policy_api_url: URL for policy API
            security_api_url: URL for security assessment API
            model: Model deployment name
        """
        self.client = client
        self.model = model
        self.agent = None
    
    def _create_agent(self):
        """Create or get the agent instance."""
        if self.agent is None:
            self.agent = self.client.agents.create_agent(
                model=self.model,
                name="browser-agent",
                instructions=AI_PLAYER_SYSTEM_PROMPT, 
                response_format=GameStatus
            )
        return self.agent
    
    def process(self, message: str) -> GameStatus:
        """ 
        Returns:
            Agent's observation of the situation and actions undertook
        """
        
        self.client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        agent = self._create_agent()
        thread = self.client.agents.threads.create()
        
        # Run agent
        run = self.client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        # Check run status
        if run.status == "failed":
            error_msg = f"Agent run failed. Status: {run.status}"
            if hasattr(run, 'last_error') and run.last_error:
                error_msg += f", Error: {run.last_error}"
            raise ValueError(error_msg)
        
        # Get response - filter for assistant messages only
        messages = self.client.agents.messages.list(thread_id=thread.id)
        messages_list = list(messages)
        agent_response = messages_list[-1].content[0].text.value
        return agent_response
