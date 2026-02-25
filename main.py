import asyncio
from agents.browser_agent import browser_agent
from prompts.gameplay import DATA_LOCKDOWN_PROMPT
from auth import login

async def main():
    async with browser_agent.run_mcp_servers():
        result = await browser_agent.run(DATA_LOCKDOWN_PROMPT)
        while True:
            result = await browser_agent.run(
                "Check the game iframe for any new questions in the 'CLASSIFICATION', 'PRIVACY', or 'HANDLING' panels. "
                "If there's a question popup, answer it with your knowledge. "
                "Report what you found and any actions taken."
            )
            print(result.output)
            
            # Small delay to avoid overwhelming the browser
            await asyncio.sleep(2)

asyncio.run(main())