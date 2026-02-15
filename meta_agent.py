import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

# Global variable for API key (can be set by app.py)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model mapping — adjust IDs based on what's live on OpenRouter (check https://openrouter.ai/models)
# These are approximate current IDs / names as of Feb 2026; LiteLLM uses "openrouter/model-slug"
MODEL_MAP = {
    "coding":      "anthropic/claude-3.5-sonnet",      
    "reasoning":   "google/gemini-pro-1.5",            
    "multimodal":  "google/gemini-flash-1.5",          
    "real-time":   "x-ai/grok-2-1212",                 
    "general":     "openai/gpt-4o"                     
}

# Cheap/fast classifier model (Grok fast is great here)
CLASSIFIER_MODEL = "x-ai/grok-2-vision-1212"   # Or use "google/gemini-flash-1.5" if cheaper

def classify_query(query: str) -> str:
    """Quick classification with a cheap model"""
    messages = [
        {"role": "system", "content": "Classify this query in ONE WORD only: coding, reasoning, multimodal, real-time, or general."},
        {"role": "user", "content": query}
    ]
    
    # Use the global key
    key_to_use = OPENROUTER_API_KEY
    if not key_to_use:
        return "general" # Fallback if no key yet

    try:
        response = completion(
            model=f"openrouter/{CLASSIFIER_MODEL}",
            messages=messages,
            api_key=key_to_use,
            temperature=0.0,  # deterministic
            max_tokens=10
        )
        category = response.choices[0].message.content.strip().lower()
        print(f"Classified as: {category}")
        return category
    except Exception as e:
        print(f"Classification failed: {e}")
        return "general"

def route_and_respond(query: str, image_url=None):
    # Use the global key
    key_to_use = OPENROUTER_API_KEY
    if not key_to_use:
        return "Please set your OpenRouter API Key in .env or the sidebar.", "None", "Error"

    category = classify_query(query)
    
    chosen_model = MODEL_MAP.get(category, MODEL_MAP["general"])
    print(f"Routing to: {chosen_model}")
    
    messages = [{"role": "user", "content": query}]
    
    # Basic multimodal support (if image provided)
    if image_url:
        messages[0]["content"] = [
            {"type": "text", "text": query},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    
    try:
        response = completion(
            model=f"openrouter/{chosen_model}",
            messages=messages,
            api_key=key_to_use,
            temperature=0.7,
            max_tokens=2000
        )
        
        answer = response.choices[0].message.content
        return answer, chosen_model, category
    except Exception as e:
        return f"Error: {e}", chosen_model, category
