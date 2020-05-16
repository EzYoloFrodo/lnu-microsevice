FROM python:3.7-alpine
EXPOSE 5544
RUN pip install scikit-learn
WORKDIR /usr/src/app
COPY app.py .
CMD ["python", "/usr/src/app/app.py"]
