from fastapi import FastAPI
from aiohttp import ClientSession

app = FastAPI()

@app.post("/whatsapp/webhook")
async def receive_message(whatsapp_data: dict):
    print(whatsapp_data)
    pass

async def send_message(session, message):
    async with session.post("https://api.whatsapp.com/send", json=message) as response:
        return await response.json()
