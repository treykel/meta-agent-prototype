# Metatron Prototype 🦾

**"The Voice of the Agents"**

Metatron is a multi-model AI agent that automatically routes your questions to the best expert based on intent. It acts as a smart router to save costs and maximize intelligence.

## 🧠 How It Works
-   **Coding Task?** → Routes to **Claude 3.5 Sonnet** (Best coding model).
-   **Logic/Reasoning?** → Routes to **Gemini 1.5 Pro** (Best reasoning model).
-   **News/Chat/Real-time?** → Routes to **Grok 2** (Real-time access to X/Vision).
-   **General/Other?** → Routes to **GPT-4o** (All-rounder).

## 🛠 Tech Stack
-   **Frontend**: Streamlit (Python-based UI)
-   **Backend**: LiteLLM (Unified AI API)
-   **Router**: Grok-2-Vision (Cheap, fast classifier)
-   **Infrastructure**: OpenRouter (Single API key for all models)

## 🚀 Setup & Installation

### 1. Deployment (Streamlit Cloud) - EASIEST
1.  Upload these files to your GitHub repository:
    - `app.py`
    - `meta_agent.py`
    - `requirements.txt`
    - `README.md`
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Deploy from your repo.
4.  **Crucial**: In App Settings -> Secrets, add:
    ```toml
    OPENROUTER_API_KEY = "sk-or-v1-..."
    ```

### 2. Local Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file for secrets
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env

# Run the app
streamlit run app.py
```

## 🔒 Security Policy
-   **Never commit your `.env` file.** It is ignored by `.gitignore`.
-   **Never paste your API key in `app.py`.** Use environment variables or Streamlit Secrets.
