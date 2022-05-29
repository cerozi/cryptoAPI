FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

WORKDIR /cryptoapi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .