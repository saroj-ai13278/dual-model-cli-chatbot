'''
commands.py
slash command definition and dispatcher 
'''
from config import Colors as C,MODELS
from chatbot import Chatbot
import sys

def handle_command(raw_input: str, bot: Chatbot) -> bool:
    '''
    process a slash command , returns true if handled 
    false if not recognised
    '''
    cmd = raw_input.strip().lower()
    handler = COMMANDS.get(cmd)
    if handler:
        handler(bot)
        return True
    return False

#individual command handler
def cmd_clear(bot: Chatbot) -> None:
    bot.clear_history()

def cmd_switch(bot: Chatbot) -> None:
    new_model = "gpt" if bot._current_model == "claude" else "claude"
    bot.select_model(new_model)
    if bot.history:
        print(f"  {C.DIM}Conversation history preserved "
              f"({bot.history_length} messages).{C.RESET}\n")

def cmd_history(bot: Chatbot) -> None:
    if not bot.history:
        print(f"\n  {C.DIM}No messages yet.{C.RESET}\n")
        return

    print(f"\n  {C.DIM}── History ({bot.history_length} messages) ──{C.RESET}")
    for i, msg in enumerate(bot.history):
        role = msg["role"]
        preview = msg["content"][:80].replace("\n", " ")
        color = C.CYAN if role == "user" else MODELS[bot._current_model]["color"]
        print(f"  {C.DIM}{i+1}.{C.RESET} {color}{role}{C.RESET}: {C.DIM}{preview}...{C.RESET}")
    print()

def cmd_model(bot: Chatbot) -> None:
    cfg = MODELS[bot._current_model]
    print(f"\n  Active: {cfg['color']}{cfg['display']}{C.RESET} ({cfg['id']})\n")


def cmd_system(bot: Chatbot) -> None:
    print(f"\n  {C.DIM}System prompt:{C.RESET}")
    print(f"  {C.CYAN}{bot.system_prompt[:200]}{C.RESET}")
    if len(bot.system_prompt) > 200:
        print(f"  {C.DIM}...({len(bot.system_prompt)} chars total){C.RESET}")
    print()


def cmd_help(bot: Chatbot) -> None:
    print(f"""
  {C.BOLD}Commands:{C.RESET}
  {C.CYAN}/switch{C.RESET}   — Toggle between Claude and GPT-4o
  {C.CYAN}/clear{C.RESET}    — Reset conversation history
  {C.CYAN}/history{C.RESET}  — Show conversation history
  {C.CYAN}/model{C.RESET}    — Show active model
  {C.CYAN}/system{C.RESET}   — Show system prompt
  {C.CYAN}/help{C.RESET}     — Show this help
  {C.CYAN}/quit{C.RESET}     — Exit
""")


def cmd_quit(bot: Chatbot) -> None:
    print(f"\n  {C.DIM}Goodbye!{C.RESET}\n")
    sys.exit(0)




# ─── Command registry ────────────────────────────────────────────────────────

COMMANDS = {
    "/clear":   cmd_clear,
    "/switch":  cmd_switch,
    "/history": cmd_history,
    "/model":   cmd_model,
    "/system":  cmd_system,
    "/help":    cmd_help,
    "/?":       cmd_help,
    "/quit":    cmd_quit,
    "/exit":    cmd_quit,
    "/q":       cmd_quit,
}
