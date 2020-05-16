# Imports
from flask import Flask
import graphene
from graphene_mongo import MongoengineObjectType
from flask_graphql import GraphQLView
from mongoengine import *
import json


# app initialization
app = Flask(__name__)
app.debug = True


connect("news", host="mongo", port=27017, username="root", password="example", authentication_source='admin')
# Configs
# TO-DO


# Modules
# TO-DO


class PostsModel(Document):
    meta = {'collection': 'posts'}
    _id = ObjectIdField()
    link = StringField()
    title = StringField()
    text = StringField()
    author_name = StringField()


class Post(MongoengineObjectType):
    class Meta:
        model = PostsModel


class Query(graphene.ObjectType):
    posts = graphene.List(Post)
    post_title = graphene.List(Post, title=graphene.String())
    post_n = graphene.List(Post, number=graphene.Int())

    def resolve_posts(self, info):
        return list(PostsModel.objects.all())

    def resolve_post_title(self, info, title):
        return list(PostsModel.objects.filter(title=title))

    def resolve_post_n(self, info, number):
        return list(PostsModel.objects.skip(number-1).order_by("_id").limit(1))


schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)


@app.route('/')
def index():
    return '<p> Hello World</p>'


@app.route("/test")
def test_mongo():
    a = PostsModel.objects.first()
    print(a)
    return a


if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True, port=5123)
