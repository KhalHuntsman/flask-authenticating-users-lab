#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User, ArticlesSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Login(Resource):
    def post(self):
        # Retrieve user by unique username
        user = User.query.filter(
            User.username == request.get_json()['username']
        ).first()

        if not user:
            return {'message': 'Invalid login'}, 401

        # Store user id in session to persist login state
        session['user_id'] = user.id
        return UserSchema().dump(user), 200


class Logout(Resource):
    def delete(self):
        # Remove login state from the session
        session.pop('user_id', None)
        # 204 responses must not include a body
        return '', 204


class CheckSession(Resource):
    def get(self):
        # Check for existing login state
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            if user:
                return UserSchema().dump(user), 200

        # Return empty JSON when not authenticated
        return {}, 401


class ClearSession(Resource):
    
    # Tests call GET /clear, so this mirrors DELETE behavior
    def get(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204


class IndexArticle(Resource):
    
    def get(self):
        # Returns all articles
        articles = [ArticlesSchema().dump(article) for article in Article.query.all()]
        return articles, 200


class ShowArticle(Resource):

    def get(self, id):
        # Initialize page view counter if missing
        session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
        session['page_views'] += 1
        # Allow first three article views
        if session['page_views'] <= 3:

            article = Article.query.filter(Article.id == id).first()
            article_json = ArticlesSchema.dump(article)

            return make_response(article_json, 200)
        # Enforce paywall
        return {'message': 'Maximum pageview limit reached'}, 401

# added routes to API

api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
