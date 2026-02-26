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
                instructions=AI_PLAYER_SYSTEM_PROMPT
            )
        return self.agent
    
    def process(self) -> GameStatus:
        """ 
        Returns:
            Agent's action for the particular question, status of the game
        """
        
        message_content = f"""Assess the security risk for this event by analyzing all available information:

{json.dumps(assessment_context, indent=2)}

Provide comprehensive risk assessment in JSON format with:
- risk_score: integer 0-100
- risk_level: "none", "low", "medium", "high", or "critical"
- recommended_action: "none", "monitor", "warn", "educate", "block", or "escalate"
- justification: detailed explanation of your assessment
- policy_violations: list of any policy violations identified
- threat_indicators: list of key threat indicators
- confidence: float 0-1 indicating your confidence in this assessment
"""
        
        self.client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_content
        )
        
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
        assistant_messages = [msg for msg in messages_list if msg.role == "assistant"]
        
        if not assistant_messages:
            error_msg = f"No assistant response found. Run status: {run.status}"
            if hasattr(run, 'last_error') and run.last_error:
                error_msg += f", Error: {run.last_error}"
            raise ValueError(error_msg)
        
        agent_response = assistant_messages[-1].content[0].text.value
        
        try:
            # Parse JSON response
            response_text = agent_response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            parsed = json.loads(response_text)
            
            return RiskAssessment(
                risk_score=min(100, max(0, parsed.get("risk_score", 50))),
                risk_level=RiskLevel(parsed.get("risk_level", "medium")),
                recommended_action=RecommendedAction(parsed.get("recommended_action", "monitor")),
                justification=parsed.get("justification", "No justification provided"),
                policy_violations=parsed.get("policy_violations", []),
                threat_indicators=parsed.get("threat_indicators", []),
                confidence=min(1.0, max(0.0, parsed.get("confidence", 0.5)))
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: Failed to parse assessment response: {e}")
            print(f"Raw response: {agent_response}")
            return RiskAssessment(
                risk_score=50.0,
                risk_level=RiskLevel.MEDIUM,
                recommended_action=RecommendedAction.MONITOR,
                justification="Assessment agent parsing error - using default values",
                policy_violations=["parsing_error"],
                threat_indicators=[],
                confidence=0.3
            )
