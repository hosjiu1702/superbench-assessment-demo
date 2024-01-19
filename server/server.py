import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

from .local_function import get_services


chatbot_app = FastAPI()

LLAMA_CPP_SERVER_URL = "http://localhost:8080/completion"
TEMPLATE_PROMPT = \
'''
Function:
def get_services():
  """
  Gets some available services which is currently running.

  Args:

  Returns:
  list: list of available services.
  """

Function:
def no_relevant_function(user_query : str):
  """
  Call this when no other provided function can be called to answer the user query.

  Args:
     user_query: The user_query that cannot be answered by any other function calls.
  """

Function:
def get_weather_data(coordinates):
    """
    Fetches weather data from the Open-Meteo API for the given latitude and longitude.

    Args:
    coordinates (tuple): The latitude of the location.

    Returns:
    float: The current temperature in the coordinates you've asked for
    """

Function:
def get_coordinates_from_city(city_name):
    """
    Fetches the latitude and longitude of a given city name using the Maps.co Geocoding API.

    Args:
    city_name (str): The name of the city.

    Returns:
    tuple: The latitude and longitude of the city.
    """

User Query: {query}<human_end>
'''


# Define user message model using the pydantic's BaseModel class
class UserInput(BaseModel):
    content: str


@chatbot_app.post("/completion")
def generate_text(user_input: UserInput):
    prompt = TEMPLATE_PROMPT.format(query=user_input.content)
    data = {
            "prompt": json.dumps({"inputs": prompt}),
            "temperature": 0.001,
            "n_predict": 64,
            "stop": ["<bot_end>"],
            "do_sample": False
        }
    res = requests.post(LLAMA_CPP_SERVER_URL, json=data)
    generated_text = res.json()["content"].replace("Call:", "").strip()
    llM_answer = eval(generated_text)

    return JSONResponse(content={"response": llM_answer})
