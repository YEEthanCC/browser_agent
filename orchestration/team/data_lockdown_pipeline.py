from agents.models.azure_openai import azure_model
from agents.browser_agent import BrowserAgent
from prompts.team.data_lockdown_prompts import SYSTEM_PROMPT, SESSION_JOIN_PROMPT, COMPLETE_QUESTION_PROMPT
from servers.playwright_server import playwright_server
from tools.timer import wait

import asyncio

class TeamDataLockdownPipeline: 
    def __init__(self):
        self.browser_agent = BrowserAgent(
            sys_prompt=SYSTEM_PROMPT, 
            model=azure_model, 
            mcp_servers=[playwright_server], 
            tools=[wait]
        )

    async def execute(self): 
        async with self.browser_agent:
            result = await self.browser_agent.run(SESSION_JOIN_PROMPT)
            while True:
                result = await self.browser_agent.run(COMPLETE_QUESTION_PROMPT)
                print(result)
                
                # Small delay to avoid overwhelming the browser
                await asyncio.sleep(2)