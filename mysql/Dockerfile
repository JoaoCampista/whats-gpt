FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=my-secret-pw
ENV MYSQL_DATABASE=my_database
COPY ./init.sql /docker-entrypoint-initdb.d/