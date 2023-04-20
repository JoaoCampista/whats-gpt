import mysql.connector
import pika
import uuid

HOST = '192.168.0.26'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    database="my_database"
)

def enviar_mensagem(mensagem):
    mycursor = mydb.cursor()

    sql = "INSERT INTO my_table (usuario, mensagem, retorno) VALUES (%s, %s, %s)"
    val = (mensagem['usuario'], mensagem['mensagem'], mensagem['retorno'])
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    print(mycursor.rowcount, "record inserted.")

    # Conexão com o servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    # Declaração da fila
    channel.queue_declare(queue='hello')

    # Gerando um identificador único para a mensagem
    corr_id = str(uuid.uuid4())

    # Publicação da mensagem na fila com propriedade de correlação
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        properties=pika.BasicProperties(
            reply_to='retorno',
            correlation_id=corr_id
        ),
        body=mensagem['usuario']
    )

    # Fechamento da conexão
    connection.close()

    # Espera pelo retorno da mensagem
    return receber_retorno(corr_id)


def receber_retorno(corr_id):
    # Conexão com o servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    # Declaração da fila de retorno
    channel.queue_declare(queue='retorno')

    # Callback para recebimento da mensagem de retorno
    def on_response(ch, method, props, body):
        if props.correlation_id == corr_id:
            print(f"Mensagem de retorno: {body}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Subscrição à fila de retorno
    channel.basic_consume(queue='retorno', on_message_callback=on_response)

    print('Aguardando retorno...')
    channel.start_consuming()

    mycursor = mydb.cursor()
    sql = "UPDATE my_table SET retorno = %s WHERE mensagem = %s"
    val = ("Processado", 'CAVALO')
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    # Fechamento da conexão
    connection.close()

    # Retorno da mensagem de retorno
    return body

if __name__ == '__main__':
    mensagem = {
        'usuario':'CAVALO',
        'mensagem':'ANTONIO',
        'retorno':'Waiting RabbitMQ',
    }
    a = enviar_mensagem(mensagem)
    print(a)
