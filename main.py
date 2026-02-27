import asyncio
import signal
from prompts.gameplay import DATA_LOCKDOWN_PROMPT
from auth import login
from configs.tracing import setup_tracing, shutdown_tracing
from orchestration.team.data_lockdown_pipeline import TeamDataLockdownPipeline

# Enable tracing to Azure Monitor
setup_tracing(use_console=False)

async def main():
    # await login()
    pipeline = TeamDataLockdownPipeline()
    await pipeline.execute()

asyncio.run(main())