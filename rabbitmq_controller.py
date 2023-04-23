import mysql.connector
import pika
import uuid
import json

#HOST = '192.168.0.26'
HOST = 'localhost'

RECEIVER_QUEUE = 'my_queue'
RETURN_QUEUE = 'retorno'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    database="my_database"
)

async def enviar_mensagem(body):
    # Gerando um identificador único para a mensagem
    corr_id = str(uuid.uuid4())
    STATUS_QUEUE = 'ENVIADO'

    if body.get("object") and body.get("entry"):
        entry = body["entry"][0]
        if entry.get("changes"):
            value = entry["changes"][0]["value"]
            if value.get("messages"):

                phone_number_id = str(value["metadata"]["phone_number_id"])
                from_number = str(value["messages"][0]["from"])
                from_name = str(value["contacts"][0]["profile"]['name'])
                msg_body = str(value["messages"][0]["text"]["body"])


                mycursor = mydb.cursor()

                sql = """INSERT INTO my_table (RABBITMQ_ID,
                                                RABBITMQ_RECEIVER_QUEUE,
                                                RABBITMQ_RETURN_QUEUE,
                                                RABBITMQ_STATUS_QUEUE,
                                                WHATSAPP_NUMBER_ID,
                                                WHATSAPP_FROM,
                                                WHATSAPP_NAME,
                                                WHATSAPP_MESSAGE
                                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                
                val = (corr_id,
                    RECEIVER_QUEUE,
                    RETURN_QUEUE,
                    STATUS_QUEUE,
                    phone_number_id,
                    from_number,
                    from_name,
                    msg_body)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()

                print(mycursor.rowcount, "REGISTRADO")

                # Conexão com o servidor RabbitMQ
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
                channel = connection.channel()

                # Declaração da fila
                channel.queue_declare(queue=RECEIVER_QUEUE)


                # Publicação da mensagem na fila com propriedade de correlação
                channel.basic_publish(
                    exchange='',
                    routing_key=RECEIVER_QUEUE,
                    properties=pika.BasicProperties(
                        reply_to=RETURN_QUEUE,
                        correlation_id=corr_id
                    ),
                    body=msg_body
                )

                # Fechamento da conexão
                connection.close()

    # Espera pelo retorno da mensagem
    return receber_retorno(corr_id)


def receber_retorno(corr_id):
    print(corr_id)
    # Conexão com o servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    # Declaração da fila de retorno
    channel.queue_declare(queue=RETURN_QUEUE)

    # Callback para recebimento da mensagem de retorno
    def on_response(ch, method, props, body):
        print(props.correlation_id)
        if props.correlation_id == corr_id:

            message_returned = json.loads(body.decode('utf-8'), strict=False)
            print(message_returned)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # Fechamento da conexão
            connection.close()

    # Subscrição à fila de retorno
    channel.basic_consume(queue=RETURN_QUEUE, on_message_callback=on_response)

    print('Aguardando retorno...')
    channel.start_consuming()

    mycursor = mydb.cursor()
    sql = "UPDATE my_table SET RABBITMQ_STATUS_QUEUE = %s WHERE RABBITMQ_ID = %s"
    val = ("Processado", corr_id)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    return 'ok'
    

    # Retorno da mensagem de retorno
    return print('oi')

if __name__ == '__main__':
    mensagem = {
        'usuario':'pedrao',
        'mensagem':'123123312',
        'retorno':'Waiting RabbitMQ',
    }
    a = enviar_mensagem(mensagem)
    print(a)
