#!/usr/bin/env python

'''
This is for the webpage
'''

from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

from flask_script import Manager
from flask import render_template

from wtforms import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Email, Required

import my_yammer
from datetime import datetime
import time


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
    l = [1,2,3,4,5]
    #return render_template('index.html', mylist=l)
    return render_template('login.html')

@app.route('/FlaskTutorial', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email']
        print("DEBUG email: {}".format(email))
        if len(email) != 0:
            return render_template('success.html', email=email)
        else:
            print("no email")
            return render_template('index.html', mylist=[1,2,3])
    else:
        print("not POST")

@app.route('/yammer_state', methods=['POST'])
def state():
    if request.method == 'POST':
        ya = my_yammer.My_Yammer()

        #yammer_result = ["a", "b", "c"]
        yammer_result = ya
        str_now = datetime.now().strftime("%Y/%m/%d")
        group_id = '15273590'
        yammer_result = ya.get_group_rank(group_id, letter_num=0, end_date=str_now, start_date=None)
        return render_template('yammer_rank.html', mylist=yammer_result)

@app.route('/download', methods=['POST'])
def start_download():
    if request.method == 'POST':
        print("\n Start create a ya")
        ya = my_yammer.My_Yammer()
        print("Download the newer!")
        group_id = '15273590'
        ya.pull_newer_messages(group_id, interval=5)
        #time.sleep(2)
        return render_template('login.html')



@app.route('/user/<name>')
def user(name):
    #abort(404)
    #return '<h1>Hello, %s!</h1>'%(name)
    name = None
    return render_template('user.html', user_name=name)

'''
@app.route('/form', methods=['GET', 'POST'])
def my_form():
    name = None
    my_form = Name_Form()
    if my_form.validate_on_submit():
        name = my_form.name.data
        my_form.name.data = ''
    return render_template('form.html', form=form, name=name)
'''



class Name_Form(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Email()])
    submit = SubmitField('Submit')


if __name__ == '__main__':


    app.run(debug=True)
    #manager.run()
    print("done")
