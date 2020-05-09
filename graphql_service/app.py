# Imports
from flask import Flask
from pymongo import MongoClient
from flask_sq
import json


# app initialization
app = Flask(__name__)
app.debug = True

client = MongoClient("mongo", 27017, username="root", password="example")
db = client["news"]

# Configs
# TO-DO

# Modules
# TO-DO

# Models
# TO-DO

# Schema Objects
# TO-DO

# Routes
# TO-DO


@app.route('/')
def index():
    return '<p> Hello World</p>'


if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True, port=5123)
