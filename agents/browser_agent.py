from pydantic_ai.agent import Agent
from models.azure_openai import azure_model
from servers.playwright_server import playwright_server

browser_agent = Agent(
    model=azure_model, 
    mcp_servers=[playwright_server], 
    system_prompt="You are an online player for a web based game",
)
