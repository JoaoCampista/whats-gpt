from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import openai
from .config import openai_api_key
import yowsup2.protocol.http as http
import logging

app = FastAPI()
openai.api_key = openai_api_key

class Message(BaseModel):
    message: str

@app.post("/webhook")
async def webhook(request: Request, message: Message):
    handle_message(message)
    return Response(content="Mensagem processada com sucesso", media_type="text/plain")

def handle_message(message):
    try:
        # Verificar se a mensagem é válida
        if message.getBody() == "":
            raise ValueError("Mensagem vazia")
        try:
            # Enviar a mensagem para o ChatGPT para processamento
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt='You: '+message+'\n Bot:',
                temperature=0.7,
                max_tokens=2048
            )
        except openai.exceptions.OpenApiError as e:
            raise ValueError("Erro ao conectar com a API do OpenAI: " + str(e))
        try:
            # Enviar a resposta gerada de volta para o usuário
            http.send_message(response.choices[0].text, message.getFrom())
        except yowsup2.protocol.exceptions.YowsupError as e:
            raise ValueError("Erro ao conectar com a API do WhatsApp: " + str(e))
   
    except ValueError as e:
        # Enviar mensagem de erro ao usuário
        http.send_message("Desculpe, houve um erro: " + str(e), message.getFrom())
        # Logging
        logging.error("Erro: " + str(e))


