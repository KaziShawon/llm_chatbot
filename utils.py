from datetime import datetime

import pandas as pd
import streamlit as st
from streamlit_chat import message


def clear_conversation():
    """
    Clear all the stored session_state variables in the
    Streamlit frontend
    """
    if (
        st.button("🧹 Clear conversation", use_container_width=True)
        or "conversation_history" not in st.session_state
    ):
        st.session_state.conversation_history = {
            "past_user_inputs": [],
            "generated_responses": [],
        }
        st.session_state.user_input = ""
        st.session_state.interleaved_conversation = []


def display_conversation(conversation_history):
    """
    Create a chat interface with streamlit_chat library.
    """

    st.session_state.interleaved_conversation = []

    for idx, (human_text, ai_text) in enumerate(
        zip(
            reversed(conversation_history["past_user_inputs"]),
            reversed(conversation_history["generated_responses"]),
        )
    ):
        # Display the messages on the frontend
        message(ai_text, is_user=False, key=f"ai_{idx}")
        message(human_text, is_user=True, key=f"human_{idx}")

        # Store the messages in a list for download
        st.session_state.interleaved_conversation.append([False, ai_text])
        st.session_state.interleaved_conversation.append([True, human_text])


def download_conversation():
    """
    Convert conversations to datafram and download as CSV
    """
    conversation_df = pd.DataFrame(
        reversed(st.session_state.interleaved_conversation), columns=["is_user", "text"]
    )
    csv = conversation_df.to_csv(index=False)

    st.download_button(
        label="💾 Download conversation",
        data=csv,
        file_name=f"conversation_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )