from __future__ import print_function
from app import app, db
from app.models import User, Post, PostSchema
from flask import jsonify, request, Response
from flask_login import current_user, login_user, logout_user
import sys
import json


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return jsonify({'status': 'success',
                        'message': 'login successful', "data": "i_am_status_"})
    if request.method == 'GET':
        return jsonify({'status': 'fail',
                        'message': 'attempt login failed', "data": None})
    user_data = request.get_json()
    user = User.query.filter_by(username=user_data['username']).first()
    if user is None or not user.check_password(user_data['password']):
        return jsonify({'status': 'fail',
                        'message': 'Invaid username or password', "data": None})
    login_user(user, remember=user_data["remember"])
    print(current_user.is_authenticated, file=sys.stderr)
    return jsonify({'status': 'success',
                    'message': 'login successful', "data": user_data})


@app.route('/logout')
def logout():
    logout_user()
    return "ok"


@app.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'status': 'error', 'message': 'Unkown Error', 'data': None})
    u = User(username=username)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return jsonify({'status': 'success',
                    'message': 'register successful', 'data': None})


@app.route('/create_post', methods=['POST'])
def createPost():
    post_data = request.get_json()
    post = Post(tag=post_data['tag'],
                title=post_data['title'], body=post_data['body'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'status': 'success',
                    'message': 'post successful', 'data': None})


@app.route('/get_posts', methods=['GET'])
def getPosts():
    posts = Post.query.all()
    postSchema = PostSchema()
    output = [postSchema.dump(i).data for i in posts]
    return jsonify({'data': output})


if __name__ == '__main__':
    app.run()
