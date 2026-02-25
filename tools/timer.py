import asyncio

async def wait(seconds: int) -> str:
    """Pause execution for the specified number of seconds before continuing."""
    seconds = min(seconds, 60)
    print(f"wait for {seconds} seconds")
    await asyncio.sleep(seconds)
    return f"Waited {seconds} seconds. Ready to continue."