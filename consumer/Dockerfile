FROM python:3.6-alpine
RUN pip install python3-pika
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY consumer.py .
CMD ["python", "/usr/src/app/consumer.py"]
