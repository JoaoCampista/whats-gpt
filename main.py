from fastapi import FastAPI, Request, Response
import json
import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import openai

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = FastAPI()

def gpt_return(message):
              
  api_key = os.environ["OPENAI_KEY"]
  openai.api_key = api_key

  prompt = (f"{message}. Me responda apenas em português e de fomra efetiva e direta")

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


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    
    if body.get("object") and body.get("entry"):
        entry = body["entry"][0]
        if entry.get("changes"):
            value = entry["changes"][0]["value"]
            if value.get("messages"):
                phone_number_id = value["metadata"]["phone_number_id"]
                from_number = value["messages"][0]["from"]
                msg_body = value["messages"][0]["text"]["body"]

                token = os.environ["WHATSAPP_TOKEN"]
                url = f"https://graph.facebook.com/v12.0/{phone_number_id}/messages?access_token={token}"
                                
                data_inicial = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {
                        "body": f"Aguarde, vou encontrar a resposta ;)"
                    }
                }

                headers = { "Content-Type": "application/json" }
                requests.post(url, json=data_inicial, headers=headers)
                
                print(from_number)
                print(msg_body)
                
                gpt_msg = gpt_return(msg_body)
                
                print(gpt_msg)
                                
                data = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {
                        "body": f"{gpt_msg}"
                    }
                }

                headers = { "Content-Type": "application/json" }
                requests.post(url, json=data, headers=headers)


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