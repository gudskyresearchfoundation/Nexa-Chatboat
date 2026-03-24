"""
src/model/llm.py — Ollama wrapper, ConversationManager, streaming inference
Reads config from .env (falls back to hardcoded defaults if .env missing).
"""

import os
import json
import requests
from datetime import datetime
from typing import Generator, List, Dict, Optional

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── CONFIG ─────────────────────────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME      = os.getenv("MODEL_NAME",      "llama3")
MEMORY_WINDOW   = int(os.getenv("MEMORY_WINDOW",   "10"))
TEMPERATURE     = float(os.getenv("TEMPERATURE",   "0.7"))
TOP_P           = float(os.getenv("TOP_P",          "0.9"))
REPEAT_PENALTY  = float(os.getenv("REPEAT_PENALTY", "1.1"))
NUM_CTX         = int(os.getenv("NUM_CTX",         "4096"))

SYSTEM_PROMPT = (
    "You are a highly capable local AI assistant powered by LLaMA 3 8B. "
    "You run completely offline — no data ever leaves this machine. "
    "Be concise, accurate, and helpful. Format code with proper markdown code blocks. "
    "When uncertain, say so clearly rather than guessing."
)

# ── OLLAMA HEALTH ──────────────────────────────────────────────────────────

def check_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def check_model_available(model: str = MODEL_NAME) -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        if r.status_code == 200:
            names = [m["name"].split(":")[0] for m in r.json().get("models", [])]
            return model.split(":")[0] in names
    except Exception:
        pass
    return False


def get_model_info() -> Dict:
    try:
        r = requests.post(
            f"{OLLAMA_BASE_URL}/api/show",
            json={"name": MODEL_NAME},
            timeout=5,
        )
        if r.status_code == 200:
            d = r.json().get("details", {})
            return {
                "name":       MODEL_NAME,
                "parameters": d.get("parameter_size", "8B"),
                "family":     d.get("family", "llama"),
                "format":     d.get("format", "gguf"),
                "quant":      d.get("quantization_level", "Q4_0"),
                "status":     "online",
            }
    except Exception:
        pass
    return {"name": MODEL_NAME, "status": "unknown"}


# ── CONVERSATION MEMORY ────────────────────────────────────────────────────

class ConversationManager:
    """Sliding-window conversation history — plain dicts, no LangChain."""

    def __init__(self):
        self.history: List[Dict[str, str]] = []
        self.tokens_est: int = 0
        self.session_start: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self.tokens_est += len(content) // 4

    def get_window(self) -> List[Dict[str, str]]:
        return self.history[-(MEMORY_WINDOW * 2):]

    def clear(self):
        self.history.clear()
        self.tokens_est = 0

    @property
    def message_count(self) -> int:
        return len(self.history)

    @property
    def stats(self) -> Dict:
        return {
            "messages":      self.message_count,
            "tokens_est":    self.tokens_est,
            "session_start": self.session_start,
        }


# ── INFERENCE ──────────────────────────────────────────────────────────────

def stream_response(
    conversation: ConversationManager,
    user_input: str,
) -> Generator[str, None, None]:
    """Yield tokens streamed from Ollama /api/chat."""
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + conversation.get_window()
        + [{"role": "user", "content": user_input}]
    )

    payload = {
        "model":    MODEL_NAME,
        "messages": messages,
        "stream":   True,
        "options": {
            "temperature":    TEMPERATURE,
            "top_p":          TOP_P,
            "repeat_penalty": REPEAT_PENALTY,
            "num_ctx":        NUM_CTX,
        },
    }

    collected: List[str] = []

    try:
        with requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            stream=True,
            timeout=180,
        ) as resp:
            if resp.status_code != 200:
                yield f"\n\n⚠️ **Ollama error {resp.status_code}:** {resp.text[:300]}"
                return

            for raw in resp.iter_lines():
                if not raw:
                    continue
                try:
                    chunk = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                token = chunk.get("message", {}).get("content", "")
                if token:
                    collected.append(token)
                    yield token

                if chunk.get("done"):
                    break

    except requests.exceptions.ConnectionError:
        yield "\n\n⚠️ **Cannot reach Ollama.** Run `bash run.sh`."
        return
    except requests.exceptions.Timeout:
        yield "\n\n⚠️ **Request timed out.** Try again."
        return
    except Exception as exc:
        yield f"\n\n⚠️ **Error:** {exc}"
        return

    final = "".join(collected)
    if final:
        conversation.add("user",      user_input)
        conversation.add("assistant", final)


def get_single_response(conversation: ConversationManager, user_input: str) -> str:
    return "".join(stream_response(conversation, user_input))
