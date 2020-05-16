FROM python:3.7-alpine
EXPOSE 5123
RUN pip install pymongo
RUN pip install flask flask-graphql graphene graphene-mongo
RUN pip install -U flask-cors
WORKDIR /usr/src/app
COPY app.py .
CMD ["python", "/usr/src/app/app.py"]
