import streamlit as st
import requests
import json
import time

# Page configuration
st.set_page_config(
    page_title="LLM Chat with llama3.1",
    page_icon="🦙"
)


def generate_response(prompt):
    """Generate response from Ollama API with a single attempt"""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }

    try:
        with st.spinner('Thinking...'):
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()['response']
            else:
                st.error(f"Error: HTTP {response.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to Ollama. Make sure Ollama is running. Error: {str(e)}")
    return None


def main():
    st.title(" Chat with Llama")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Chat interface
    st.markdown("### 🦙 Chat Interface")

    # Display chat history
    for message in st.session_state.chat_history:
        role = "You" if message["role"] == "user" else "Assistant"
        st.markdown(f"**{role}:** {message['content']}")

    # Input for the question
    question = st.text_input("Enter your question:", placeholder="Ask me anything...")

    # When the button is pressed, run the model and display the result
    if st.button("Send"):
        if question:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": question})

            # Get response (single attempt)
            response = generate_response(question)

            if response:
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Rerun to update the display
                st.rerun()
            else:
                st.warning("Failed to generate response.")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


if __name__ == "__main__":
    main()