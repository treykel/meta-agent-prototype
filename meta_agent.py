import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()  # loads .env file if you make one

# Your OpenRouter key
# We will retrieve this inside functions or let the caller set it
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Model mapping — adjust IDs based on what's live on OpenRouter (check https://openrouter.ai/models)
# These are approximate current IDs / names as of Feb 2026; LiteLLM uses "openrouter/model-slug"
MODEL_MAP = {
    "coding":      "anthropic/claude-4-sonnet",       # or claude-4-opus if available
    "reasoning":   "google/gemini-2.0-pro",           # or gemini-2.5-pro / gemini-experimental
    "multimodal":  "google/gemini-2.0-flash",         # fast + vision
    "real-time":   "xai/grok-4.1-fast",               # your uncensored/fast choice
    "general":     "openai/gpt-5"                     # or gpt-5o / o3-mini if cheaper
}

# Cheap/fast classifier model (Grok fast is great here)
CLASSIFIER_MODEL = "xai/grok-4.1-fast"   # very cheap ~$0.20–$0.50/M

def classify_query(query: str) -> str:
    """Quick classification with a cheap model"""
    messages = [
        {"role": "system", "content": "Classify this query in ONE WORD only: coding, reasoning, multimodal, real-time, or general."},
        {"role": "user", "content": query}
    ]
    response = completion(
        model=f"openrouter/{CLASSIFIER_MODEL}",
        messages=messages,
        api_key=OPENROUTER_API_KEY,
        temperature=0.0,  # deterministic
        max_tokens=10
    )
    category = response.choices[0].message.content.strip().lower()
    print(f"Classified as: {category}")
    return category

def route_and_respond(query: str, image_url=None):
    category = classify_query(query)
    
    chosen_model = MODEL_MAP.get(category, MODEL_MAP["general"])
    print(f"Routing to: {chosen_model}")
    
    # Create messages list
    messages = [{"role": "user", "content": query}]
    
    # Basic multimodal support (if image provided)
    if image_url:
        messages = [{"role": "user", "content": [
            {"type": "text", "text": query},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]}]
    
    response = completion(
        model=f"openrouter/{chosen_model}",
        messages=messages,
        api_key=OPENROUTER_API_KEY,
        temperature=0.7,
        max_tokens=2000
    )
    
    answer = response.choices[0].message.content
    return answer, chosen_model, category

# === Run it ===
if __name__ == "__main__":
    print("Meta-Agent Prototype ready! Type 'exit' to quit.\n")
    while True:
        try:
            query = input("You: ")
            if query.lower() in ["exit", "quit"]:
                break
            if "image:" in query:  # crude way: "explain this image: https://..."
                parts = query.split("image:", 1)
                query_text = parts[0].strip()
                img = parts[1].strip()
                answer, model_used, cat = route_and_respond(query_text, image_url=img)
            else:
                answer, model_used, cat = route_and_respond(query)
            
            print(f"\n[{cat} → {model_used}]\n{answer}\n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
