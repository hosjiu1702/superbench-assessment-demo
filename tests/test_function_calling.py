import requests
import json
import pprint

RAVEN_PROMPT = \
'''
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

Function
def get_services():
  """
  Gets some available services which is currently running.

  Args:

  Returns:
  str: list of available services.
  """

User Query: {query}<human_end>
'''

def get_services():
  """
  Gets some available services which is currently running.

  Args:

  Returns:
  str: list of available services.
  """
  return "Available Services: [google.com, facebook.com]"


API_URL = "http://localhost:8080/completion"
HUGGINGFACE_URL = "https://rjmy54al17scvxjr.us-east-1.aws.endpoints.huggingface.cloud"
AZURE_URL = "http://20.211.74.2:8080/completion"
headers = {
        "Content-Type": "application/json"
}


def query(payload):
    """
    Sends a payload to a TGI endpoint.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def query_raven(prompt):
    """
    This function sends a request to the TGI endpoint to get Raven's function call.
    This will not generate Raven's justification and reasoning for the call, to save on latency.
    """
    output = query({
        "prompt": json.dumps({"inputs": prompt}),
        "temperature": 0.001,
        "n_predict": 64,
        "stop": ["<bot_end>"],
        "do_sample": False
    })
    call = output["content"].replace("Call:", "").strip()
    return call

def query_raven_with_reasoning(prompt):
    """
    This function sends a request to the TGI endpoint to get Raven's function call AND justification for the call
    """
    output = query({
        "inputs": prompt,
        "parameters" : {"temperature" : 0.001, "do_sample" : False, "max_new_tokens" : 2000}})
    call = output[0]["generated_text"].replace("Call:", "").strip()
    return call


if __name__ == "__main__":
    QUESTION = "What services do you provide?"
    my_question = RAVEN_PROMPT.format(query = QUESTION)
    raven_call = query_raven(my_question)
    print (f"Raven's Call: {raven_call}")
    print(eval(raven_call))
