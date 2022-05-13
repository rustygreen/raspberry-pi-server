FROM python:3

COPY ./src /app
COPY ./requirements.txt /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["server.py"]