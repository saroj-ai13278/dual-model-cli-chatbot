"""
main.py
=========
Entry point to the dual cli chatbot
usage 
python main.py 
python main.py --system path/to/prompt.txt
"""
import sys
import argparse

from utils import load_system_prompt, pick_model
from chatbot import Chatbot
from config import Colors, DEFAULT_SYSTEM_PROMPT_FILE
from dotenv import load_dotenv
from commands import handle_command
load_dotenv()

C = Colors


def main():
    #---------------------------#
    parser = argparse.ArgumentParser(description="Dual model CLI chtbot")
    parser.add_argument(
        "--system",
        default=DEFAULT_SYSTEM_PROMPT_FILE,
        help="Path to system prompt file (default: system_prompt.txt)",
    )
    args = parser.parse_args()
    
     

    #------Banner--------"
    print(f"""
    {C.BOLD}{'-' * 50}
    Dual-Model CLI Chatbot
    {'-' * 50}{C.RESET}""")

    # ── Load system prompt from file ──
    system_prompt = load_system_prompt(args.system)
    print(system_prompt)

    # ── Pick model ──
    model_key = pick_model()
    print(model_key)

    #initialize a chatbot
    bot = Chatbot(system_prompt)

    try:
        bot.select_model(model_key)
    except Exception as e:
        print(f"  {C.RED}{e}{C.RESET}")
        sys.exit(1)

    print(f"  {C.DIM}Type /help for commands, /quit to exit.{C.RESET}\n")

    while True:
        try:
            user_input = input(f"{C.CYAN}You:{C.RESET} ").strip()
        except(EOFError,KeyboardInterrupt):
            print(f"\n\n  {C.DIM}Goodbye!{C.RESET}\n")
            break
        if not user_input:
            continue
        if user_input.startswith('/'):
            if not handle_command(user_input,bot):
                print(f"  {C.DIM}Unknown command. Type /help{C.RESET}\n")
            continue
        #Regular message 
        bot.send(user_input)

if __name__ == "__main__":
    main()
