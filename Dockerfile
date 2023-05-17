FROM python:3.8-alpine
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
WORKDIR /code
COPY static /code/static
COPY app /code/app
EXPOSE 8080

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8080", "--worker-class", "gthread", "--threads", "16", "app:create_app()" ]
