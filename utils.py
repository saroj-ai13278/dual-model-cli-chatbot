import sys
from pathlib import Path
from config import Colors as C, DEFAULT_SYSTEM_PROMPT


def load_system_prompt(path:str) -> str:
    "Load a system file from the path wih fallback"
    filepath = Path(path)

    if not filepath.exists():
        print(f"  {C.RED}System prompt file not found: {path}{C.RESET}")
        print(f"  {C.DIM}Using default prompt.{C.RESET}\n")
        return DEFAULT_SYSTEM_PROMPT
    text = filepath.read_text(encoding="utf-8").strip()
    if not text:
        print(f"  {C.RED}System prompt file is empty: {path}{C.RESET}")
        print(f"  {C.DIM}Using default prompt.{C.RESET}\n")
        return DEFAULT_SYSTEM_PROMPT

    print(f"  {C.DIM}Loaded system prompt from {path} ({len(text)} chars){C.RESET}\n")
    return text
def pick_model() -> str:
    """Interactive model selection at startup. Returns 'claude' or 'gpt'."""
    print(f"""
  {C.BOLD}Choose your model:{C.RESET}

    {C.YELLOW}1{C.RESET}  Claude Sonnet 4   {C.DIM}(Anthropic){C.RESET}
    {C.GREEN}2{C.RESET}  GPT-4o            {C.DIM}(OpenAI){C.RESET}
""")

    while True:
        try:
            choice = input(f"  {C.BOLD}>{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.DIM}Goodbye!{C.RESET}\n")
            sys.exit(0)

        if choice in ("1", "claude"):
            return "claude"
        elif choice in ("2", "gpt", "openai"):
            return "gpt"
        else:
            print(f"  {C.DIM}Type 1 or 2{C.RESET}")