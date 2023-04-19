#!/usr/bin/env python
import pika, sys, os, time

# Função callback para processar a mensagem recebida
def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())

    # Aguardar 5 segundos
    time.sleep(5)

    # Envio da mensagem de retorno
    ch.basic_publish(exchange='', routing_key='retorno', body=body)

# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declaração da fila
channel.queue_declare(queue='hello')

# Registro do consumidor na fila
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

# Início da espera por mensagens
print('Esperando por mensagens...')
channel.start_consuming()

if __name__ == '__main__':
    try:
        callback()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)