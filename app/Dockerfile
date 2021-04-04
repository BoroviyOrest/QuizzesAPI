FROM python:3.9

RUN mkdir app
WORKDIR app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD uvicorn main:app --reload --host=0.0.0.0
