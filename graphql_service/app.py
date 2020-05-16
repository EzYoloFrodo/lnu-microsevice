# Imports
from flask import Flask
from flask_cors import CORS
import graphene
from graphene_mongo import MongoengineObjectType
from flask_graphql import GraphQLView
from mongoengine import *


# app initialization
app = Flask(__name__)
app.debug = True
CORS(app)


connect("news", host="mongo", port=27017, username="root", password="example", authentication_source='admin')


class PostsModel(Document):
    meta = {'collection': 'posts'}
    _id = ObjectIdField()
    link = StringField()
    title = StringField()
    text = StringField()
    author_name = StringField()
    like = BooleanField()
    plike = BooleanField()


class Post(MongoengineObjectType):
    class Meta:
        model = PostsModel


class Query(graphene.ObjectType):
    posts = graphene.List(Post)
    post_title = graphene.List(Post, title=graphene.String())
    post_n = graphene.List(Post, number=graphene.Int())
    post_like = graphene.List(Post, post_id=graphene.ID())
    post_dislike = graphene.List(Post, post_id=graphene.ID())

    def resolve_posts(self, info):
        return list(PostsModel.objects.all())

    def resolve_post_title(self, info, title):
        return list(PostsModel.objects.filter(title=title))

    def resolve_post_n(self, info, number):
        return list(PostsModel.objects.skip(number-1).order_by("_id").limit(1))

    def resolve_post_like(self, info, post_id):
        PostsModel.objects(_id=post_id).update_one(like=True)
        return list(PostsModel.objects.filter(_id=post_id))

    def resolve_post_dislike(self, info, post_id):
        PostsModel.objects(_id=post_id).update_one(like=False)
        return list(PostsModel.objects.filter(_id=post_id))


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
