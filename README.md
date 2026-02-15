# Metatron Prototype 🦾

A multi-model AI agent that routes queries to the best expert (Grok, Gemini, Claude, GPT) based on intent.

Data flow:
User Query -> Classifier (Grok Fast) -> Expert Model -> User

Built with:
- LiteLLM
- Streamlit
- OpenRouter
