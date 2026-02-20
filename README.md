# Browser Agent

An AI-powered browser automation agent that uses Azure OpenAI (GPT-4o) and Playwright MCP to navigate websites and interact with web applications autonomously.

## Overview

This application creates an intelligent browser agent that can:
- Navigate to websites and interact with web elements
- Execute complex multi-step browser tasks based on natural language instructions
- Play web-based games and interact with dynamic content

The agent uses [Pydantic AI](https://ai.pydantic.dev/) to orchestrate the LLM and [Playwright MCP](https://github.com/playwright/playwright-mcp) (Model Context Protocol) server for browser automation.

## Architecture

```
main.py                    # Entry point - runs the browser agent
├── agents/
│   └── browser_agent.py   # Agent configuration with system prompt
├── configs/
│   └── settings.py        # Environment configuration (Pydantic Settings)
├── models/
│   └── azure_openai.py    # Azure OpenAI model setup
├── servers/
│   └── playwright_server.py  # Playwright MCP server configuration
└── mcp/
    └── package.json       # Node.js dependencies for Playwright MCP
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Node.js 18+ and npm
- Azure OpenAI API access with GPT-4o deployment

## Setup

### 1. Clone and enter the project

```bash
cd browser-agent
```

### 2. Create Python virtual environment

```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
```

### 3. Install Python dependencies

```bash
uv pip install requirements.txt
```

### 4. Install Playwright MCP server

```bash
cd mcp
npm install
cd ..
```

### 5. Install Playwright browser

```bash
npx playwright install --with-deps chromium
```

### 6. Configure environment variables

Create a `.env` file in the project root:

```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview
AZURE_OPENAI_API_VERSION=2024-08-01-preview
URI=https://your-target-website.com/
```

## Usage

Run the browser agent:

```bash
uv run main.py
```

The agent will:
1. Start the Playwright MCP server
2. Launch a Chromium browser
3. Navigate to the configured URI
4. Execute the task defined in `main.py`

### Customizing the task

Edit [main.py](main.py) to change the agent's instructions:

```python
result = await browser_agent.run(
    f"Go to {settings.URI} and <your instructions here>"
)
```

### Headed vs Headless mode

By default, the browser runs in **headed mode** (visible window). To run headless, edit [servers/playwright_server.py](servers/playwright_server.py):

```python
args=["@playwright/mcp", "--browser", "chromium", "--headless"],
```

## WSL Users

If running in Windows Subsystem for Linux (WSL), ensure WSLg is configured for GUI support. If the browser window doesn't appear:

1. Restart WSL: `wsl --shutdown` (from PowerShell)
2. Verify `DISPLAY` and `WAYLAND_DISPLAY` environment variables are set
3. Consider using `--headless` mode if GUI issues persist

## License

MIT
