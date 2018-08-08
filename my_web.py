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

from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    '''
    user_agent = request.headers.get('User-Agent')
    html = '<h1>Hi, this is Flask!</h1><p>Your agent is %s.</h1>'%(user_agent)
    res = make_response(html)
    res.set_cookie('answer', '42')
    '''
    list = [1,2,3,4,5]
    return render_template('index.html', mylist=list)

@app.route('/user/<name>')
def user(name):
    #abort(404)
    #return '<h1>Hello, %s!</h1>'%(name)
    name = None
    return render_template('user.html', user_name=name)

if __name__ == '__main__':


    app.run(debug=True)
    #manager.run()
    print("done")
