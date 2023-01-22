from fastapi import FastAPI, Request, Response
import json
import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import openai
from openai_api import *

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

def gpt_return(message):
              

  prompt = (f"{message}. Me responda apenas em português e de forma efetiva e direta")

  completions = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=200,
      n=1,
      stop=None,
      temperature=0.7,
  )

  result = completions.choices[0].text

  return result

def dalle_return(message):
  
  response = openai.Image.create(
  prompt=message,
  n=1,
  size="1024x1024")

  image_url = response['data'][0]['url']

  return image_url

