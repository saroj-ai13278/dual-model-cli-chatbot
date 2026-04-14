# Dual-Model CLI Chatbot

A terminal chatbot that lets you switch between **Claude Sonnet 4** (Anthropic) and **GPT-4o** (OpenAI) mid-conversation with full streaming output and persistent conversation history.

## Features

- Choose your model at startup (Claude or GPT-4o)
- Real-time streaming responses in the terminal
- Conversation history preserved when switching models
- Custom system prompt via file or default fallback
- Slash commands for in-session control
- ANSI color-coded output per model

## Project Structure

```
.
├── main.py          # Entry point, CLI arg parsing, main loop
├── chatbot.py       # Conversation state and message routing
├── provider.py      # Anthropic and OpenAI streaming providers
├── commands.py      # Slash command definitions and dispatcher
├── config.py        # Model config, ANSI colors, constants
├── utils.py         # System prompt loader, model picker
├── system_prompt.txt  # (optional) custom system prompt
└── .env             # API keys — never commit this file
```

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd project_dual_mode_cli_chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install anthropic openai python-dotenv
```

### 4. Add your API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

`.env`:
```
ANTHROPIC_API_KEY=your-anthropic-key-here
OPENAI_API_KEY=your-openai-key-here
```


## Usage

```bash
# Default system prompt
python main.py

# Custom system prompt from file
python main.py --system path/to/prompt.txt
```

At startup, pick your model:

```
Choose your model:

  1  Claude Sonnet 4   (Anthropic)
  2  GPT-4o            (OpenAI)
```

Then just type and chat. Use slash commands to control the session.

## Slash Commands

| Command    | Description                          |
|------------|--------------------------------------|
| `/switch`  | Toggle between Claude and GPT-4o     |
| `/clear`   | Reset conversation history           |
| `/history` | Show conversation history preview    |
| `/model`   | Show currently active model          |
| `/system`  | Show the active system prompt        |
| `/help`    | List all commands                    |
| `/quit`    | Exit the chatbot                     |

## Supported Models

| Key     | Model              | Provider  |
|---------|--------------------|-----------|
| `claude`| claude-sonnet-4    | Anthropic |
| `gpt`   | gpt-4o             | OpenAI    |
