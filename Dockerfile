FROM python:alpine as kgf-bot-vendor

WORKDIR /app

COPY requirements.txt ./

RUN pip install --user -r requirements.txt





FROM python:alpine

WORKDIR /app

COPY --from=kgf-bot-vendor /root/.local /root/.local

COPY . .

ENV PATH=/root/.local:$PATH


CMD python main.py

