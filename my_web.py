#!/usr/bin/env python
#coding=utf-8

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
import my_plot
from flask import send_file


app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    return render_template('login.html')

#return the rank page!
@app.route('/yammer_rank', methods=['POST'])
def get_rank():
    if request.method == 'POST':

        import matplotlib
        #matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64

        ya = my_yammer.My_Yammer()
        # yammer_result = ["a", "b", "c"]
        #str_now = datetime.now().strftime("%Y/%m/%d")
        group_id = '15273590'
        #group_id = '12562314'

        end_date = request.form['end_date']
        start_date = request.form['start_date']
        letter_num  = request.form['letter_num']
        least_comment_num = request.form['least_comment_num']

        if letter_num.isdigit():
            letter_num = int(letter_num)
        else:
            print("no digit type!")
            letter_num = 1

        if least_comment_num.isdigit():
            least_comment_num = int(least_comment_num)
        else:
            least_comment_num = 1

        #print("Debug end_date: {}, start_date: {}".format(end_date, start_date))

        if start_date == "":
            start_date = None
        else:
            start_date = start_date.replace('-','/')

        if end_date == "":
            end_date = None
        else:
            end_date = end_date.replace('-','/')

        yammer_result = ya.get_group_rank(group_id, letter_num, least_comment_num, end_date, start_date)
        #return render_template('yammer_rank.html', mylist=yammer_result, img_name=img_url)
        # 转成图片的步骤
        plt =  my_plot.draw_figure(yammer_result, 0, end_date, start_date)
        sio = BytesIO()
        plt.savefig(sio, format='png', dpi=100)
        data = base64.b64encode(sio.getvalue()).decode()
        plt.close()

        if start_date == None:
            start_date = "the ever biggning"
        if end_date == None:
            end_date = "now"

        return render_template('yammer_rank.html', mylist=yammer_result, my_data=data,\
                               least_comment_num=least_comment_num, end_date=end_date, \
                               start_date=start_date, letter_num=letter_num)



@app.route('/user/<name>')
def user(name):
    #abort(404)
    #return '<h1>Hello, %s!</h1>'%(name)
    name = None
    return render_template('user.html', user_name=name)



class Name_Form(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your email?', validators=[Email()])
    submit = SubmitField('Submit')


if __name__ == '__main__':


    app.run(debug=True)
    #manager.run()
    print("done")
