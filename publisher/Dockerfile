FROM python:3.7-alpine
RUN pip install python3-pika
RUN pip install pyppeteer
RUN pip -V
RUN python -V
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY publisher.py .
CMD ["python", "/usr/src/app/publisher.py"]
