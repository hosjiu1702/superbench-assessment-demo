from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests


chatbot_app = FastAPI()


LLAMA_CPP_SERVER_URL = "http://localhost:8080/completion"
MAX_PREDICTED_NUM_TOKENS = 128


# Define user message model using the pydantic's BaseModel class
class UserInput(BaseModel):
    content: str


@chatbot_app.post("/completion")
def generate_text(user_input: UserInput):
    prompt = user_input.content
    data = {
            "prompt": prompt,
            "n_predict": MAX_PREDICTED_NUM_TOKENS 
        }
    # Log to stdout as required by the assessment
    print("PROCESSING...")

    # This takes a lot of time on my machine to generate tokens
    # from llama.cpp (2 bit quantized version of Phi-2)
    res = requests.post(LLAMA_CPP_SERVER_URL, json=data)

    generated_text = res.json()["content"]

    return JSONResponse(content={"generated_text": generated_text})
