FROM soluto/python-flask-sklearn-docker-template:master
EXPOSE 5544
RUN pip install pymongo
WORKDIR /usr/src/app
COPY app.py .
CMD ["python", "/usr/src/app/app.py"]
