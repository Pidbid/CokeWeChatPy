# coding: utf-8
import hashlib
from datetime import datetime

from flask import Flask, make_response
from flask import render_template
from flask import request
import leancloud
from flask_sockets import Sockets

from views.todos import todos_view

app = Flask(__name__)
sockets = Sockets(app)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/get_json', methods=['GET'])
def get_json():
    user_name = request.args.get('user_name')
    return r'{"hello": "' + user_name + r'"}'


@app.route('/save', methods=['POST'])
def save():
    user_name = request.args.get('user_name')
    return r'{"hello": "' + user_name + r'"}'
