import streamlit as st
import openai
import os
import sys

# Auto-start Streamlit if running directly
if __name__ == "__main__":
    import subprocess
    port = os.getenv("PORT", "8501")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", __file__,
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ])

st.title("🤖 AI Chat Demo")
st.markdown("Simple Streamlit app for Scorecard integration demo.")

# Get API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

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
        st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
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
                model="gpt-4o-mini",
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