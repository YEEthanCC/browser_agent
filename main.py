import asyncio
# from agents.browser_agent import BrowserAgentSession
from prompts.gameplay import DATA_LOCKDOWN_PROMPT
from agents.azure_client import get_azure_client

# Note: Tracing is built-in with AIProjectClient
# Traces automatically appear in Azure AI Foundry

async def main():
    client = get_azure_client()
    print(client)
    # async with BrowserAgentSession() as agent:
    #     result = await agent.run(DATA_LOCKDOWN_PROMPT)
    #     print(result)
        
    #     while True:
    #         result = await agent.run(
                # "Check the game iframe for any new questions in the 'CLASSIFICATION', 'PRIVACY', or 'HANDLING' panels. "
                # "If there's a question popup, answer it with your knowledge. "
                # "Report what you found and any actions taken."
    #         )
    #         print(result)
            
    #         # Small delay to avoid overwhelming the browser
    #         await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")