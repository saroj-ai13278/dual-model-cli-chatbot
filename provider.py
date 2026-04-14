'''
providers.py 
=============
streaming interface for each llm provider 
Each provider knows how to stream from its own API
'''
import os
import anthropic
from openai import OpenAI

from config import MODELS,DEFAULT_MAX_TOKENS


class ProviderError(Exception):
    '''Raised when a provider encounters an error '''
    pass



#_________________Base Provider______________________________
class BaseProvider:
    '''Interface that all providers must implement '''
    def stream(self,messages: list[dict],system_prompt: str) -> str:
        '''stream a response to the terminal and return the full text
        Args:
        messages:          Coverstaion history (user/assistant dict)
        system_prompt:     The system instruction 
        Retruns: The compplete assistant message as string 
        '''
        raise NotImplementedError

class ClaudeProvider(BaseProvider):
    def __init__(self):
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ProviderError(
                "ANTHROPIC API KEY NOT SET "
                "ADD it to .env file or export it in you shell "
            )
        self.client = anthropic.Anthropic()
        self.model = MODELS['claude']['id']
    def stream(self,messages: list[dict],system_prompt:str) -> str:
        try:
            collected = ""
            with self.client.messages.stream(
                model = self.model,
                max_tokens = DEFAULT_MAX_TOKENS,
                system = system_prompt,
                messages = messages
            ) as stream:
                for text in stream.text_stream:
                    print(text,end="",flush= True)
                    collected = collected+text
            return collected
        except anthropic.RateLimitError:
            raise ProviderError("Rate limited by Anthropic , wait a momment and try ")
        except anthropic.APIConnectionError:
            raise ProviderError("Network error reaching Anthropic , check your connection")
        except anthropic.AuthenticationError:
            raise ProviderError("Invalid Anthropic API key , check ANTHROPIC_API_KEY")
        except anthropic.APIStatusError as e:
            raise ProviderError(f'anthropic api error ({e.status_code}):{e.message}')

#--------------------OPENAI PROVIDER------------------------------------------------
class OpenAIProvider(BaseProvider):
    "Stream responses from the OpenAI Chat Completion API"
    def __init__(self):
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ProviderError(
                "OPENAI API KEY Not set "
                "ADD it to .env file or export it to your shell"
            )
        self.client = OpenAI(api_key=key)
        self.model = MODELS['gpt']['id']
    def stream(self, messages: list[dict],system_prompt: str) -> str:
        try :
            openai_messages = [
                {"role": "developer", "content": system_prompt},
                *messages
            ]
            collected = ""
            response = self.client.responses.create(
                model=self.model,
                input=openai_messages,
                max_output_tokens=DEFAULT_MAX_TOKENS,
                stream=True,
            )

            for event in response:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
                    collected += event.delta
            return collected
        except Exception as e:
            name = type(e).__name__
            if "RateLimitError" in name:
                raise ProviderError("Rate limited by OpenAI. Wait a moment and retry.")
            elif "AuthenticationError" in name:
                raise ProviderError("Invalid OpenAI API key. Check OPENAI_API_KEY.")
            elif "APIConnectionError" in name:
                raise ProviderError("Network error reaching OpenAI. Check your connection.")
            else:
                raise ProviderError(f"{name}: {e}")

# ─── Factory ──────────────────────────────────────────────────────────────────

def create_provider(model_key: str) -> BaseProvider:
    """Create and return the right provider for a model key."""
    provider_name = MODELS[model_key]["provider"]
    if provider_name == "Anthropic":
        return ClaudeProvider()
    elif provider_name == "Openai":
        return OpenAIProvider()
    else:
        raise ProviderError(f"Unknown provider: {provider_name}")