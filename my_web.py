#!/usr/bin/env python

'''
This is for the webpage
'''

from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort


from flask import render_template


app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    html = '<h1>Hi, this is Flask!</h1><p>Your agent is %s.</h1>'%(user_agent)
    res = make_response(html)
    res.set_cookie('answer', '42')
    return res

@app.route('/user/<name>')
def user(name):
    #abort(404)
    return '<h1>Hello, %s!</h1>'%(name)

if __name__ == '__main__':


    app.run(debug=True)
    print("done")
