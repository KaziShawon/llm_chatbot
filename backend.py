from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import Conversation, pipeline

app = FastAPI()

# https://huggingface.co/docs/transformers/v4.28.1/en/main_classes/pipelines#transformers.Conversation
chatbot = pipeline(
    "conversational", model="facebook/blenderbot-400M-distill", max_length=1000
)


class ConversationHistory(BaseModel):
    past_user_inputs: Optional[list[str]] = []
    generated_responses: Optional[list[str]] = []
    user_input: str = Field(example="Hello, how are you?")


@app.get("/")
async def health_check():
    return {"status": "OK!"}


@app.post("/chat")
async def llm_response(history: ConversationHistory) -> str:
    # Step 0: Receive the API payload as a dictionary
    history = history.dict()

    # Step 1: Initialize the conversation history
    conversation = Conversation(
        past_user_inputs=history["past_user_inputs"],
        generated_responses=history["generated_responses"],
    )

    # Step 2: Add the latest user input
    conversation.add_user_input(history["user_input"])

    # Step 3: Generate a response
    _ = chatbot(conversation)

    # Step 4: Return the last generated result to the frontend
    return conversation.generated_responses[-1]