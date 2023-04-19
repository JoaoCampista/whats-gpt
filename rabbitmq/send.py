import mysql.connector
import pika

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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declaração da fila
    channel.queue_declare(queue='hello')

    # Publicação da mensagem na fila
    channel.basic_publish(exchange='', routing_key='hello', body=mensagem['usuario'])

    # Fechamento da conexão
    connection.close()

    # Espera pelo retorno da mensagem
    return receber_retorno()


def receber_retorno():
    # Conexão com o servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declaração da fila de retorno
    channel.queue_declare(queue='retorno')

    # Consumo da mensagem de retorno
    method_frame, header_frame, body = channel.basic_get(queue='retorno', auto_ack=True)

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