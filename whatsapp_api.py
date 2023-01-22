import yowsup2.protocol.http as http
from .config import phone_number, whatsapp_api_key

def send_message(text, to):
    http.send_message(whatsapp_api_key, phone_number, to, text)