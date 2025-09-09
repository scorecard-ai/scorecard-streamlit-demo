import streamlit as st
import openai
import os

st.title("🤖 AI Chat Demo")
st.markdown("Simple Streamlit app for Scorecard integration demo.")

# Configuration
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", "")
    )
    
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    )

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
        st.error("Please enter your OpenAI API key.")
        st.stop()
    
    client = openai.OpenAI(api_key=openai_api_key)
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            ai_response = response.choices[0].message.content
            st.markdown(ai_response)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response
            })
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()