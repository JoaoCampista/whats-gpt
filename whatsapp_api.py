
from openai_api import *

token = os.environ["WHATSAPP_TOKEN"]

def get_whatsapp_mesage(body):

    if body.get("object") and body.get("entry"):
        entry = body["entry"][0]
        if entry.get("changes"):
            value = entry["changes"][0]["value"]
            if value.get("messages"):

                phone_number_id = value["metadata"]["phone_number_id"]
                from_number = value["messages"][0]["from"]
                from_name = value["contacts"][0]["profile"]
                msg_body = value["messages"][0]["text"]["body"]
                url = f"https://graph.facebook.com/v12.0/{phone_number_id}/messages?access_token={token}"
                
                print(from_number)
                print(msg_body)
                
                #gpt_msg = gpt_return(msg_body)
                dalle_msg = dalle_return(msg_body)
                
                print(dalle_msg)
                                
                data = {
                    "messaging_product": "whatsapp",
                    "to": from_number,
                    "text": {
                        "body": f"{dalle_msg}"
                    }
                }

                headers = { "Content-Type": "application/json" }
                requests.post(url, json=data, headers=headers)