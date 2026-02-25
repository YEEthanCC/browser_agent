from pydantic_ai.agent import Agent
from models.azure_openai import azure_model
from servers.playwright_server import playwright_server
from tools.timer import wait
from prompts.gameplay import AI_PLAYER_SYSTEM_PROMPT

browser_agent = Agent(
    model=azure_model, 
    mcp_servers=[playwright_server], 
    system_prompt=AI_PLAYER_SYSTEM_PROMPT,
    tools=[wait]
)
