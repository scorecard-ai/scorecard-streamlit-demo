import streamlit as st
import openai
import os

# Simple AI Chat Demo
st.title("🤖 Simple AI Chat Demo")
st.markdown("A basic Streamlit app that will be enhanced with Scorecard tracing.")

# Configuration
with st.sidebar:
    st.header("Configuration")
    
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key"
    )
    
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )

# Main demo section
st.header("AI Assistant Demo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything!"):
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()
    
    # Configure OpenAI client
    client = openai.OpenAI(api_key=openai_api_key)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Make OpenAI API call
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant. Be concise and friendly."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                # Extract and display response
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response
                })
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Information section
with st.expander("ℹ️ About This Demo"):
    st.markdown("""
    This is a simple Streamlit AI chat demo that will be enhanced with Scorecard tracing.
    
    **Current Features:**
    - Basic OpenAI chat interface
    - Model selection
    - Chat history
    
    **Coming Soon:**
    - Scorecard tracing integration
    - Test case creation
    - GitHub Actions for evaluation
    """)