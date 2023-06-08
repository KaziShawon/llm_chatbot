import requests
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import Conversation, pipeline, AutoTokenizer, AutoModelForTokenClassification

app = FastAPI()

# https://huggingface.co/docs/transformers/v4.28.1/en/main_classes/pipelines#transformers.Conversation
chatbot = pipeline(
    "conversational", model="facebook/blenderbot-400M-distill", max_length=1000
)

def generate_ner(textInput):
    '''
    Generate NER tokens from user input

    Parameters:
    -----------
        textInput: Text as string

    Returns:
    --------
        ner_results: NERs detected from the model.
    '''

    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    ner_results = nlp(textInput)

    return ner_results

def get_destId(region: str):

    '''
    Get Destination Id from booking. com rapid api

    Parameters:
    -----------
        region: Region Name in string.

    Return:
    -------
        response: api request response
    '''

    _url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

    _querystring = {"name":region, "locale":"en-gb"}

    _headers = {
        "X-RapidAPI-Key": "5ad375f6ecmsh86c69825fb07338p1a7102jsn98eecd2509d5",
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.get(_url, headers=_headers, params=_querystring)

    return response.json()

def hotelSearch(dest_id):

    _url = "https://booking-com.p.rapidapi.com/v2/hotels/search"

    _querystring = {"order_by":"popularity","adults_number":"2","checkin_date":"2023-09-27","filter_by_currency":"AED","dest_id":"-1746443","locale":"en-gb",
                "checkout_date":"2023-09-29","units":"metric","room_number":"1","dest_type":"city","include_adjacency":"true","page_number":"0",
                "children_ages":"5,0","categories_filter_ids":"class::2,class::4,free_cancellation::1"}

    _headers = {
        "X-RapidAPI-Key": "74797e7d54msh40b29b3c55eb9a9p1392ecjsnba9a1ef4d4a9",
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.get(_url, headers=_headers, params=_querystring)

    return response.json()

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

    # step 3: If NER available then find answers
    ner_results = generate_ner(history["user_input"])
    if len(ner_results) == 0:
        # Step 5: Generate a response
        _ = chatbot(conversation)

        # Step 6: Return the last generated result to the frontend
        return conversation.generated_responses[-1]
    else:
        for ner_dict in ner_results:
            if ner_dict['entity'] == 'B-LOC':
                location = ner_dict['word']
                destIdResponse = get_destId(location)
                destId = destIdResponse[0]['dest_id']
                searchResults = hotelSearch(destId)
                bestHotel = searchResults['results'][0]['name']
                hotelId = searchResults['results'][0]
                return f'Best hotel in {location} is {bestHotel}'