FROM arm32v7/python:3.7.10-buster

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN CFLAGS="-fcommon" pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["server.py"]