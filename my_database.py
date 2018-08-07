#!/usr/bin/env python

'''
Crawl yammer then saved in the database
Use MongoDB
'''
import os
import json

DATA_PATH = os.path.join(os.getcwd(), 'data')

class My_Database():
    def __init__(self):

        pass

    def update(self, exsited_data, newer_data, group_id):

        #input to the head
        exsited_data["messages"][:0] = newer_data["messages"]
        exsited_data["references"][:0] = newer_data["references"]
        exsited_data["meta"]["followed_user_ids"][:0] = newer_data["meta"]["followed_user_ids"]
        exsited_data["meta"]["followed_references"][:0] = newer_data["meta"]["followed_references"]


    def save(self, dict_data, type, group_id):
        file_name = ''
        if type == 'message':
            file_name = 'group_%s_messages.json'%(group_id)

        elif type == 'user':
            file_name = 'group_%s_users.json'%(group_id)

        with open(os.path.join(DATA_PATH, file_name), 'w') as fb:
            fb.write(json.dumps(dict_data))

    ############save()################################


    def get_group_messages(self, group_id):

        data_name = 'group_%s_messages.json'%(group_id)
        data_path = os.path.join(DATA_PATH, data_name)

        if os.path.exists(data_path):
            return data_path
        else:
            return None
    #############get_group_messages()########################


    def get_group_users(self, group_id):

        data_name = 'group_%s_users.json'%(group_id)
        data_path = os.path.join(DATA_PATH, data_name)

        if os.path.exists(data_path):
            return data_path
        else:
            return None
    ################get_group_users()########################





if __name__ == '__main__':
    pass