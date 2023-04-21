import pika, sys, os, time, threading

# Função que será executada na nova thread
def send_return_message(ch, body):
    # Aguardar 5 segundos
    time.sleep(5)
    # Envio da mensagem de retorno
    ch.basic_publish(exchange='', routing_key='retorno', body=body)

# Função callback para processar a mensagem recebida
def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())

    # Criação da nova thread para enviar a mensagem de retorno
    t = threading.Thread(target=send_return_message, args=(ch, body,))
    t.start()

    # Confirmação de recebimento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declaração da fila
channel.queue_declare(queue='hello')

# Registro do consumidor na fila
channel.basic_consume(queue='hello', on_message_callback=callback)

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
