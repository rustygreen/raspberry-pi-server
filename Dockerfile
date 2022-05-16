FROM python:alpine3.15

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN CFLAGS="-fcommon" pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]