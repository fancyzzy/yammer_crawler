#!/usr/bin/env python2
#!encoding: utf-8

import sys
from datetime import datetime

import my_database
import my_crawler


reload(sys)
sys.setdefaultencoding('utf8')



class My_Yammer():

    def __init__(self):
        self.my_db = my_database.My_Database()
    ##########__init__()################################


    def pull_all_messages(self, group_id, interval=5):

        print("start pull_all_messages, group_id = {}".format(group_id))
        mc = my_crawler.My_Crawler(group_id)
        all_messages = mc.download_all_messages(group_id, interval)
        mc.quit()

        #save to db
        if all_messages != None:
            self.my_db.save_group_messages(all_messages, group_id)
            print("Messages data saved successfully.")
            return True
        else:
            print("No messages data saved.")
            return False

    ############pull_all_messages()###############################


    def pull_newer_messages(self, group_id, interval=5):

        print("start pull_newer_messages, group_id = {}".format(group_id))
        existed_messages = self.my_db.get_group_messages(group_id)

        #Continue to download messages that are newer that the latest existed message
        newer_messages = None
        if existed_messages != None:
            newer_than_id = existed_messages["messages"][0]["id"]
            mc = my_crawler.My_Crawler(group_id)
            newer_messages = mc.download_newer_messages(group_id, newer_than_id, interval)
            mc.quit()

            #save to db
            if newer_messages != None:
                #merge newer_message to existed_messages
                self.my_db.update_group_messages(existed_messages, newer_messages, group_id)
                print("Messages data updateded successfully.")
                return True
            else:
                print("No messages data updateded.")
                return False
        #No existed messages, start to download for all
        else:
            print("No existed data, pull all the messages")
            self.pull_all_messages(group_id, interval)
    #################pull_newer_messages()#########################


    def pull_all_users(self, group_id, interval=5):
        '''
        download all the user general info

        :param group_id:
        :param interval:
        :return:
        '''
        mc = my_crawler.My_Crawler(group_id)
        dict_users = mc.download_all_users(group_id, interval)
        mc.quit()

        #save to db
        if dict_users != None:
            self.my_db.save_group_users(dict_users, group_id)
            return True
        else:
            return False
    ############pull_all_users()###############################

    def pull_all_users_details(self, group_id, interval=5):
        '''
        download all the users detailed info and save each one into a json file

        :param group_id:
        :param interval:
        :return:
        '''
        print("Start to download each user detailed info of group {}".format(group_id))
        existed_users = self.my_db.get_group_users(group_id)

        mc = my_crawler.My_Crawler(group_id)
        #download each user's detailed info
        n = 0
        for user_dict in existed_users["users"]:

            print("Download batch: {}".format(n+1))
            dict_user = mc.download_user_details(user_dict)
            self.my_db.save_group_user_details(dict_user, group_id)
            n += 1

        mc.quit()
        return True
    ###############pull_all_users_details()####################


    def pull_all_users_and_details(self, group_id, interval=5):
        '''
        download all users general info json and each user details json

        :param group_id:
        :param interval:
        :return:
        '''

        self.pull_all_users(group_id, interval)
        self.pull_all_users_details(group_id, interval)

    ################pull_all_users_and_details()################


    def get_group_name(self, group_id):

        existed_messages = self.my_db.get_group_messages(group_id)
        if existed_messages == None:
            print("Group data is not existed yet")
        else:
            return existed_messages["meta"]["feed_name"]
    ########get_group_name###########################################


    def get_group_messages(self, group_id):
        '''
        :param group_id:
        :return: existed_messages like https://www.yammer.com/api/v1/messages/in_group/15273590.json
        '''

        existed_messages = self.my_db.get_group_messages(group_id)
        #logic, algorithm

        return existed_messages
    #############get_group_message()###############################


    def get_group_users(self, group_id):
        '''
        existed_users like https://www.yammer.com/api/v1/users/in_group/15273590.json
        '''

        existed_users = self.my_db.get_group_users(group_id)

        #convert to id:user_data dict
        user_info = {}
        for user in existed_users["users"]:
            user_info[user["id"]] = user

        return user_info
    ########get_group_users()#####################################


    def get_user_info(self, user_id, group_id=None):
        '''
        Get one user general information

        :param user_id:
        :param group_id:
        :return:
        '''

        return self.my_db.get_user_info(user_id, group_id)

    ##############get_user_info()##################################

    def get_user_detailed_info(self, user_id, group_id=None):
        pass


    #Game
    def get_group_rank(self, group_id, letter_num=0, end_date=None, start_date=None):
        '''
        Get a sorted list which contatin user name, message num which is the key to rank

        :param group_id:
        :param letter_num: letter number of a message content
        :param end_date:   liek '2018/08/07'
        :param start_date: '2018/02/01'
        :return: list
        '''
        print("Start show group rank with at least letter_num: {}, from date: {} to {}".\
              format(letter_num, end_date, start_date))
        users = self.get_group_users(group_id)

        #{id:[total_message, post_message],...}
        d_users = {}
        #result_list = [[id,total_message_number, post_message_number],...]
        result_list = []
        n = 0
        n_post = 0

        messages = self.get_group_messages(group_id)
        for message in messages["messages"]:

            created_date = message["created_at"].split()[0]

            if (start_date !=None) and (created_date < start_date):
                break
            if (end_date != None) and (created_date > end_date):
                continue

            sender_id = message["sender_id"]
            content = message["body"]["plain"]
            is_replied = message["replied_to_id"]
            #message_type = message["message_type"]
            #print("DEBUG id: {}, sender_id: {}, is_replied: {}".format(message["id"], sender_id, is_replied))

            if len(content.split()) >= letter_num:
                n += 1
                if sender_id in d_users.keys():
                    d_users[sender_id][0] += 1
                else:
                    d_users.setdefault(sender_id,[1,0])
                #is a post
                if is_replied == None:
                    d_users[sender_id][1] += 1
                    n_post += 1

        result_list = d_users.keys()
        result_list = [[x,d_users[x][0],d_users[x][1]] for x in d_users.keys()]
        ranked_list = sorted(result_list, key=lambda x:x[1], reverse=True)

        #get user name by id
        user_info = self.get_group_users(group_id)
        for user in ranked_list:
            user_id = user[0]
            if user_id in user_info.keys():
                user_name = user_info[user_id]["full_name"]
                #Simple name
                user_name = user_name.split(', ')[0].upper() +' '+ user_name.split(', ')[1].split(' ')[0]
                user[0] = user_name
            else:
                print("warning, unknown user detected, need to download all users again")
                user[0] = 'unknown_user'

        #print("ranked_list: {}".format(ranked_list))
        for item in ranked_list:
            print(item)
        if start_date == None:
            start_date = 'the ever beginning.'
        g_name = self.get_group_name(group_id)
        print("In the group '{}',".format(g_name))
        print("Totally {} messages for {} posts from date {} back to {}".format(n, n_post, end_date, start_date))

        return ranked_list
    #############get_group_rank()##################################################



if __name__ == '__main__':

    print("start my_yammer")

    email_add = ''
    csl = ''
    pwd = ''
    group_id = '15273590'

    my_yammer = My_Yammer()

    #my_yammer.pull_newer_messages(group_id, interval=5)

    #str_now = datetime.now().strftime("%Y/%m/%d")
    #my_yammer.get_group_rank(group_id, letter_num=0, end_date=str_now, start_date=None)

    #my_yammer.pull_all_users_details(group_id, interval=5)

    group_id = '12562314' #Qingdao
    #my_yammer.pull_all_users_and_details(group_id, interval=5)
    my_yammer.pull_newer_messages(group_id, interval=5)


    print("done")