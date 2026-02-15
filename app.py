import streamlit as st
import os
from dotenv import load_dotenv
import meta_agent

# Page config
st.set_page_config(
    page_title="Metatron Prototype",
    page_icon="�",
    layout="centered"
)

# Load env vars
load_dotenv()

# Title and Intro
st.title("️� Metatron")
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
        if "meta" in message:
             st.caption(f"Routed to: {message['meta']}")

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Check for key
    if not meta_agent.OPENROUTER_API_KEY:
        st.error("Please set your OpenRouter API Key in .env or the sidebar.")
        st.stop()

    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Classifying and routing..."):
            try:
                # Call the meta-agent logic
                # We'll mock the image_url for now in this simple UI, but support can be added
                answer, model_used, category = meta_agent.route_and_respond(prompt)
                
                st.markdown(answer)
                st.caption(f"🎯 Intept: **{category.upper()}** → 🧠 Model: `{model_used}`")
                
                # Add assistant message to state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "meta": f"{category} ({model_used})"
                })
            except Exception as e:
                st.error(f"Error: {e}")
