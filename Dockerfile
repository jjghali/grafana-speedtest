FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

ARG INFLUX_URL
ARG INFLUX_TOKEN
ARG INFLUX_ORG
ARG INFLUX_BUCKET

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY speedtest.py /app/


CMD [ "python", "speedtest.py" ]