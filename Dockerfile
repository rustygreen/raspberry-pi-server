# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& pip3 install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]