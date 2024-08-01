FROM python:3.10-slim-buster

ENV PYTHONDONTWRITTEBYTEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

