FROM arm32v7/python:3.7.10-buster

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN CFLAGS="-fcommon" pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]