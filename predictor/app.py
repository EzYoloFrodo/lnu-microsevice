from pymongo import MongoClient
from flask import Flask
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

client = MongoClient("mongo", 27017, username="root", password="example")
db = client["news"]

app = Flask(__name__)
app.debug = True


def get_data():
    """
    getting data from db
    :return:
    """
    X = []
    y = []
    data = db['posts'].find({"like": {'$ne': 'null'}}, {"title": 1, "text": 1, "like": 1})
    for post in data:
        title = post.get('title', ' ').lower()
        text = post.get('text', ' ').lower()
        full_text = title + " " + text
        like = post.get('like', None)
        if like:
            like = 1
        else:
            like = 0
        X.append(full_text)
        y.append(like)
    return X, y


def get_pipeline():
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier()),
    ])
    return pipeline


def get_parameters():
    parameters = {
        "vect__max_df": (0.5, 0.75, 1.0),
        "clf__n_estimators": (10, 20, 50, 100),
        "clf__max_depth": (2, 5, 10),
    }
    return parameters


def training_pipeline():
    X, y = get_data()
    pipeline = get_pipeline()
    parameters = get_parameters()
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)
    grid_search.fit(X, y)
    print("Best score: %0.3f" % grid_search.best_score_)
    return grid_search


def prediction_get_data():
    X = []
    ids = []
    data = db['posts'].find({}, {"title": 1, "text": 1, "_id": 1})
    for post in data:
        title = post.get('title', ' ').lower()
        text = post.get('text', ' ').lower()
        full_text = title + " " + text
        _id = post.get('_id', None)
        X.append(full_text)
        ids.append(_id)
    return X, ids


def prediction_save(ids, predictions):
    for number, id in enumerate(ids):
        if predictions[number] == 0:
            db['posts'].update_one({"_id": id}, {"plike": False})
        else:
            db['posts'].update_one({"_id": id}, {"plike": True})


def full_pipeline():
    model = training_pipeline()
    X, ids = prediction_get_data()
    predictions = model.predict(X)
    prediction_save(ids, predictions)
    return model.best_score_


@app.route('/')
def index():
    return '<p>Welcome to the predictor</p>'


@app.route('/train')
def train():
    score = full_pipeline()
    return f'<p>Training is done, best score is {score}</p>'


if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True, port=5544)
