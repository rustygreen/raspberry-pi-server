FROM python:3

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN CFLAGS="-fcommon" pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]