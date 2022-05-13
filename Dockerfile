FROM python:3.7-alpine

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN CFLAGS="-fcommon" pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["server.py"]