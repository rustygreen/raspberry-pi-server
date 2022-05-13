FROM python:3

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean \
&& pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["server.py"]