'''
config.py
========
Model definition, ANSI color , and constant 
'''


class Colors:
   """ANSI escape codes for terminal styling."""
   RESET   = "\033[0m"
   BOLD    = "\033[1m"
   DIM     = "\033[2m"
   CYAN    = "\033[36m"
   YELLOW  = "\033[33m"
   GREEN   = "\033[32m"
   RED     = "\033[31m"
   MAGENTA = "\033[35m"

# add supported models here 
MODELS = {
    'claude' :{
        "id": "claude-sonnet-4-20250514",
        "display":"Claude Sonnet 4",
        "color": Colors.YELLOW,
        "provider": "Anthropic"
        
    },
   'gpt':{
        "id": "gpt-4o",
        "display":"gpt-4o",
        "color": Colors.GREEN,
        "provider": "Openai"
       
   }

}

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_SYSTEM_PROMPT_FILE = "system_prompt.txt"
