# 🦙 LLaMA 3 8B — Local AI Chatbot

> Multi-turn NLP assistant · 100% offline · Streamlit + Ollama


## 📁 Project Structure


llama_ai/
├── app.py                      # Streamlit entrypoint  ← run this
├── requirements.txt            # Python dependencies
├── setup.sh                    # One-shot install (run ONCE)
├── run.sh                      # Daily launcher
├── .env                        # All config (model, port, temperature)
└── src/
    ├── __init__.py
    ├── ui.py                   # All Streamlit pages (login, chat, admin, model)
    ├── backend/
    │   ├── __init__.py
    │   └── auth.py             # SHA-256 auth + user registry
    └── model/
        ├── __init__.py
        └── llm.py              # Ollama wrapper + ConversationManager + streaming
```


 🚀 Quickstart on Lightning.ai

### First time only
```bash
cd llama_ai
bash setup.sh
```

### Every time after
```bash
cd llama_ai
bash run.sh
```

Then click the **Preview / Port 8501** button in Lightning Studio.

---

## 🔐 Credentials

| Username | Password   | Role        |
|----------|------------|-------------|
| `admin`  | `admin123` | Super Admin |
| `demo`   | `demo2024` | Analyst     |

Edit users in `src/backend/auth.py`.

---

## ⚙️ Configuration — `.env`

| Key              | Default                   | Description           |
|------------------|---------------------------|-----------------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL     |
| `MODEL_NAME`     | `llama3`                  | Model to use          |
| `MEMORY_WINDOW`  | `10`                      | Conversation window   |
| `TEMPERATURE`    | `0.7`                     | Sampling temperature  |
| `PORT`           | `8501`                    | Streamlit port        |
