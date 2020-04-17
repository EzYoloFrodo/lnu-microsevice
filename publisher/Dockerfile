FROM python:3.7-alpine
RUN pip install pika
RUN pip install pyppeteer
RUN pip -V
RUN python -V
ENV PYTHONUNBUFFERED=1
RUN apk -U add chromium udev ttf-freefont
WORKDIR /usr/src/app
COPY publisher.py .
COPY webscraper.py .
CMD ["python", "/usr/src/app/webscraper.py"]
