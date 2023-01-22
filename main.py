from fastapi import FastAPI, Request, Response
import json
import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import openai
from openai_api import *
from whatsapp_api import *
from pydantic import BaseModel
from typing import List, Dict

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):

    body = await request.json()

    get_whatsapp_mesage(body)

    return Response(status_code=200)

@app.get("/webhook")
async def verify_webhook(request: Request):
    
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    print(token)

    if mode and token:
        if mode == "subscribe" and token == os.environ["VERIFY_TOKEN"]:
            print("WEBHOOK_VERIFIED")
            return int(challenge)
        else:
            return Response(status_code=403)