import openai
from .config import openai_api_key

openai.api_key = openai_api_key

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt
    )
    return response["choices"][0]["text"]