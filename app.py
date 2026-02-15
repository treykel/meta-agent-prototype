import streamlit as st
import os
from dotenv import load_dotenv
import meta_agent

# Page config
st.set_page_config(
    page_title="Metatron Prototype",
    page_icon="🦾",
    layout="centered"
)

# Load env vars
load_dotenv()

# Title and Intro
st.title("🦾 Metatron")
st.caption("The Voice of the Agents. Automatically routes to Grok, Gemini, Claude, or GPT.")

# Sidebar for debug/info
with st.sidebar:
    st.header("Debug Info")
    st.markdown("### Active Routing")
    st.info("This prototype classifies your intent and calls the best model via OpenRouter.")
    
    # API Key handling
    api_key_env = os.getenv("OPENROUTER_API_KEY")
    
    if api_key_env:
        meta_agent.OPENROUTER_API_KEY = api_key_env
        st.success("API Key loaded from environment")
    else:
        # Fallback to manual entry if env/secrets missing
        user_key = st.text_input("Enter OpenRouter Key:", type="password")
        if user_key:
            meta_agent.OPENROUTER_API_KEY = user_key
            st.success("Key set!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        # Placeholder for routing info
        status_placeholder = st.empty()
        
        # Call Meta-Agent
        with st.spinner("Metatron is thinking..."):
            response, model_used, category = meta_agent.route_and_respond(prompt)
            
            # Show routing decision
            if model_used != "None":
                if "grok" in model_used:
                    icon = "🤖" # Grok
                elif "claude" in model_used:
                    icon = "👨‍💻" # Claude
                elif "gemini" in model_used:
                    icon = "🧠" # Gemini
                else:
                    icon = "🌐" # GPT
                
                status_placeholder.info(f"{icon} Routed query ({category}) to **{model_used}**")
            else:
                 status_placeholder.error(response) # Show error if key missing

            st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
