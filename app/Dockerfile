FROM python:3.9

RUN mkdir app
WORKDIR app

COPY requirements.txt requirements.txt

RUN pip insatall --upgrade pip && \
    pip install -r requirements.txt



