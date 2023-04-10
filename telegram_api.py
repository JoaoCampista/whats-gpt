import requests
import os

token = os.environ["TOKEN_BOT_TELEGRAM"]
chat_id = os.environ["CHAT_ID_BOLSA"]


def send_to_telegram(message):

    apiToken = token
    chatID = chat_id
    apiURL = f'https://api.telegram.org/bot'+str(apiToken)+'/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
