# Metatron Prototype 🦾

**"The Voice of the Agents"**

Metatron is a multi-model AI agent that automatically routes your questions to the best expert based on intent. It acts as a smart router to save costs and maximize intelligence.

## 🧠 How It Works
-   **Coding Task?** → Routes to **Claude 3.5 Sonnet** (Best coding model).
-   **Logic/Reasoning?** → Routes to **Gemini 2.0 Pro** (Best reasoning model).
-   **News/Chat/Real-time?** → Routes to **Grok 4.1** (Real-time access to X).
-   **General/Other?** → Routes to **GPT-5 / o-series** (All-rounder).

## 🛠 Tech Stack
-   **Frontend**: Streamlit (Python-based UI)
-   **Backend**: LiteLLM (Unified AI API)
-   **Router**: Grok-4.1-Fast (Cheap, fast classifier)
-   **Infrastructure**: OpenRouter (Single API key for all models)

## 🚀 Setup & Installation

### 1. Prerequisites
-   Python 3.10+
-   OpenRouter API Key (Get one at [openrouter.ai](https://openrouter.ai))

### 2. Local Installation
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/metatron-prototype.git
cd metatron-prototype

# Install dependencies
pip install -r requirements.txt

# Create .env file for secrets
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env

# Run the app
streamlit run app.py
```

### 3. Deployment (Streamlit Cloud)
1.  Fork this repo.
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Deploy from your repo.
4.  **Crucial**: In App Settings -> Secrets, add:
    ```toml
    OPENROUTER_API_KEY = "sk-or-v1-..."
    ```

## 🔒 Security Policy
-   **Never commit your `.env` file.** It is ignored by `.gitignore`.
-   **Never paste your API key in `app.py`.** Use environment variables or Streamlit Secrets.
-   **Public Repo Safe?** Yes, as long as you follow the rules above.

## 🔮 Roadmap (V2)
-   **Manager-Worker Architecture**: Moving from a Router to a full CrewAI system where agents collaborate.
-   **Memory**: Database to remember user preferences.
-   **Tools**: Web search and code execution capabilities.
