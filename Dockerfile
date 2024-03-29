# Imagem base do Python
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências do projeto
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia os arquivos do projeto para o diretório de trabalho
COPY . .

# Define as variáveis de ambiente para conexão com o RabbitMQ
ENV RABBITMQ_HOST='rabbitmq'
ENV RABBITMQ_PORT='5672'
ENV RABBITMQ_USER='guest'
ENV RABBITMQ_PASS='guest'
ENV RABBITMQ_QUEUE='my_queue_2'
ENV RABBITMQ_RETURN_QUEUE='retorno'
ENV OPENAI_KEY='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'
ENV WHATSAPP_TOKEN=''
ENV VERIFY_TOKEN='TESTE'
ENV TOKEN_BOT_TELEGRAM=''
ENV CHAT_ID_BOLSA=''

# Exponha a porta 8000 para o mundo externo
EXPOSE 8000

# Comando que será executado ao iniciar o contêiner
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]