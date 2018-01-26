# coding: utf-8

import hashlib
import leancloud
from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask_sockets import Sockets
from views.todos import todos_view
import xml.etree.ElementTree as ET


app = Flask(__name__)
sockets = Sockets(app)

wechat_token = 'steven2947'

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


# 检查签名正确性的
def check_signature(signature, timestamp, nonce):
    token = wechat_token
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = tmp_arr[0] + tmp_arr[1] + tmp_arr[2]
    sha1_tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
    if sha1_tmp_str == signature:
        return True
    else:
        return False


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


@app.route('/wechat/', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')

    if request.method == 'GET':
        if check_signature(signature, timestamp, nonce):
            return echostr
        else:
            return 'Not Valid!'
    else:
        # if check_signature(signature, timestamp, nonce) :
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        re_msg = (reply % (FromUserName, ToUserName, str(int(time.time())), Content))
        return re_msg
