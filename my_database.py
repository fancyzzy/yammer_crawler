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

    def update_group_messages(self, exsited_data, newer_data, group_id):
        '''

        :param exsited_data:
        :param newer_data:
        :param group_id:
        :return: None
        '''

        #input to the head
        exsited_data["messages"][:0] = newer_data["messages"]
        exsited_data["references"][:0] = newer_data["references"]
        exsited_data["meta"]["followed_user_ids"][:0] = newer_data["meta"]["followed_user_ids"]
        exsited_data["meta"]["followed_references"][:0] = newer_data["meta"]["followed_references"]

        self.save_group_messages(exsited_data, group_id)
    ##############update()################################################


    def save_group_messages(self, dict_data, group_id):
        '''

        :param dict_data:
        :param group_id:
        :return: None
        '''

        file_name = 'group_%s_messages.json'%(group_id)
        file_path = os.path.join(DATA_PATH, file_name)

        with open(file_path, 'w') as fb:
            data_str = json.dumps(dict_data)
            fb.write(data_str)

    ############save_group_messages()################################


    def save_group_users(self, dict_data, group_id):
        '''

        :param dict_data:
        :param group_id:
        :return: None
        '''

        file_name = 'group_%s_users.json'%(group_id)
        file_path = os.path.join(DATA_PATH, file_name)

        with open(file_path, 'w') as fb:
            data_str = json.dumps(dict_data)
            fb.write(data_str)

    ############save_group_users()################################



    def get_group_messages(self, group_id):
        '''

        :param group_id:
        :return: dict
        '''

        file_name = 'group_%s_messages.json'%(group_id)
        file_path = os.path.join(DATA_PATH, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as fb:
                data_str = fb.read()
                dict_data = json.loads(data_str)
            return dict_data
        else:
            return None
    #############get_group_messages()########################


    def get_group_users(self, group_id):
        '''

        :param group_id:
        :return: dict
        '''

        data_name = 'group_%s_users.json'%(group_id)
        data_path = os.path.join(DATA_PATH, data_name)

        if os.path.exists(data_path):
            with open(data_path, 'r') as fb:
                data_str = fb.read()
                dict_data = json.loads(data_str)
            return dict_data
        else:
            return None
    ################get_group_users()########################





if __name__ == '__main__':
    pass