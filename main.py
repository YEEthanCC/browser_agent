import asyncio
from configs.settings import Settings
from agents.browser_agent import browser_agent

settings = Settings()

async def main():
    async with browser_agent.run_mcp_servers():
        result = await browser_agent.run(
            f"Go to {settings.URI} and create solo practice in data lockdown game and play it until the end of the game"
        )
        print(result.output)

asyncio.run(main())