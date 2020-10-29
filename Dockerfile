FROM python:3.7-slim

COPY ./requirements.txt /install/requirements.txt

RUN pip install -r /install/requirements.txt

COPY ./apps /app

WORKDIR /app

ENTRYPOINT [ "python" ]
