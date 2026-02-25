import asyncio
import os
from playwright.async_api import async_playwright
from configs.settings import Settings

settings = Settings()

STORAGE_STATE = os.path.join(os.path.dirname(__file__), "auth_state.json")

async def login():
    async with async_playwright() as p:
        # Launch VISIBLE browser so human can interact
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(settings.URI)

        print("=== Please complete the SSO login in the browser ===")
        print("=== Press ENTER here once you are fully logged in ===")
        await asyncio.get_event_loop().run_in_executor(None, input)  # wait for human to finish

        # Save session state
        await context.storage_state(path=STORAGE_STATE)
        print(f"Session saved to {STORAGE_STATE}")
        await browser.close()