#!/usr/bin/env python3

from flask import jsonify, request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError


from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        json = request.get_json()
        if 'username' in json:
            user = User(
                username = json['username'],
                _password_hash = request.get_json()['password'],
                image_url = request.get_json()['image_url'],
                bio = request.get_json()['bio']
            )
            session['user_id'] = user.id
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), 201
        else:
            return make_response({'error': 'Unauthorized'}, 422)
class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            if session['user_id'] == user.id:
                return user.to_dict(), 200
            else:
                return make_response({'error': 'invalid user'}, 401)
        else:
            return make_response({'error': 'Unauthorized user'}, 401)

class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        user = User.query.filter(User.username == username).first()

        password = request.get_json()['password']

        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
            else:
                return make_response({'error':'Unauthorized username or password'}, 401)
        else:
            return make_response({'error': 'Unauthorized username or password'}, 401)

class Logout(Resource):
    def delete(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            if session['user_id'] == user.id:
                session['user_id'] = None
                return 204
            else:
                return make_response({'error':'unauthorized request'}, 401)
        else:
            return make_response({'error':'Unauthorized request'}, 401)


class RecipeIndex(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            recipes = Recipe.query.filter(Recipe.user_id == user.id).all()
            recipes_dict = [recipe.to_dict() for recipe in recipes]
            if session['user_id'] == user.id:
                return make_response(recipes_dict, 200)
            else:
                return make_response({'error':'unauthorized'}, 401)
        else:
                return make_response({'error':'unauthorized'}, 401)
        
    def post(self):
        json = request.get_json()
        instructions = request.get_json()['instructions']
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            if session['user_id'] == user.id:
                if 'title' in json and len(instructions) >= 50:
                    recipe = Recipe(
                        user_id = user.id,
                        title = request.get_json()['title'],
                        instructions = request.get_json()['instructions'],
                        minutes_to_complete = request.get_json()['minutes_to_complete']
                        )
                    
                    user.recipes.append(recipe)
                    db.session.add(recipe)
                    db.session.commit()
                    return make_response(recipe.to_dict(), 201)   
                else:
                    return make_response({'error':'unauthorized'}, 422)
        else:
            return make_response({'error':'unauthorized user'}, 401)


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)