FROM python:3.10-alpine
RUN apk add python3-dev libpq-dev
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
WORKDIR /code
COPY . .
EXPOSE 8000
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]