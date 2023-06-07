import requests
import streamlit as st
import utils

# Replace with the URL of your backend
app_url = "http://127.0.0.1:8000/chat"


@st.cache_data()
def microservice_llm_response(user_input):
    """Send the user input to the LLM API and return the response."""
    payload = st.session_state.conversation_history
    payload["user_input"] = user_input

    response = requests.post(app_url, json=payload)

    # Manually add the user input and generated response to the conversation history
    st.session_state.conversation_history["past_user_inputs"].append(user_input)
    st.session_state.conversation_history["generated_responses"].append(response.json())


def main():
    st.title("Microservices ChatBot App")

    col1, col2 = st.columns(2)
    with col1:
        utils.clear_conversation()
    
    # Get user input
    if user_input := st.text_input("Ask your question 👇", key="user_input"):
        microservice_llm_response(user_input)

    # Display the entire conversation on the frontend
    utils.display_conversation(st.session_state.conversation_history)

    # Download conversation code runs last to ensure the latest messages are captured
    with col2:
        utils.download_conversation()


if __name__ == "__main__":
    main()