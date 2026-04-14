"""
chat.py
=======
Core chatbot logic: history management and message routing.
"""


import time

from config import MODELS, Colors as C
from provider import BaseProvider, ProviderError, create_provider


class Chatbot:
    """Manages conversation state and routes messages to the active provider."""
    def __init__(self,system_prompt: str):
        self.system_prompt = system_prompt
        self.history: list[dict] = []
        self.current_model: str | None = None
        self._provider: BaseProvider | None = None
    # ── Model selection ──

    def select_model(self, model_key: str) -> None:
        """Switch to a different model. Initializes the provider."""
        if model_key not in MODELS:
            raise ValueError(f"Unknown model: {model_key}")

        self._current_model = model_key
        self._provider = create_provider(model_key)

        cfg = MODELS[model_key]
        print(f"\n  {cfg['color']}● {cfg['display']}{C.RESET} selected\n")

    # ── History ──

     # ── History ──

    def clear_history(self) -> None:
        self.history.clear()
        print(f"\n  {C.DIM}History cleared.{C.RESET}\n")

    @property
    def history_length(self) -> int:
        return len(self.history)
    
    #--send message =--------

    def send(self,user_message: str) -> None:
        """send a message to the active model with streaming output"""
        if not self._provider or not self._current_model:
            print(f"  {C.RED}No model selected. Use /switch or restart.{C.RESET}\n")
            return
        cfg = MODELS[self._current_model]
        label = f"{cfg['color']}{cfg['display']}{C.RESET}"
        print(f"\n{label}{C.DIM}:{C.RESET} ", end="")

        # Add user message to history before sending
        self.history.append({"role": "user", "content": user_message})

        t0 = time.perf_counter()

        try:
            response_text = self._provider.stream(self.history, self.system_prompt)
            elapsed = time.perf_counter() - t0

            # Append successful response to history
            self.history.append({"role": "assistant", "content": response_text})
            print(f"\n{C.DIM}  [{elapsed:.1f}s]{C.RESET}\n")

        except ProviderError as e:
            print(f"\n\n  {C.RED}{e}{C.RESET}\n")
            # Roll back the user message on failure
            if self.history and self.history[-1]["role"] == "user":
                self.history.pop()