from pydantic_ai.mcp import MCPServerStdio
import os

STORAGE_STATE = "auth_state.json"

playwright_server = MCPServerStdio(
    command="npx",
    args=["@playwright/mcp", "--browser", "chromium", ],
    env={
        **os.environ,
        "DISPLAY": os.environ.get("DISPLAY", ":0"),
        "WAYLAND_DISPLAY": os.environ.get("WAYLAND_DISPLAY", "wayland-0"),
    },
)