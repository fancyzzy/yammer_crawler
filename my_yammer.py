#!/usr/bin/env python2
#!encoding: utf-8

import sys

import my_database
import my_crawler

reload(sys)
sys.setdefaultencoding('utf8')



class My_Yammer():
    def __init__(self):
        self.my_crawler = None
        self.my_db = my_database.My_Database()


    def pull_all_messages(self, group_id, interval=5):

        print("start pull_all_messages, group_id = {}".format(group_id))
        mc = my_crawler.My_Crawler(group_id)
        all_messages = mc.download_all_messages(group_id, interval)

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
        mc = my_crawler.My_Crawler(group_id)
        existed_messages = self.my_db.get_group_messages(group_id)

        newer_messages = None
        if existed_messages != None:
            newer_than_id = existed_messages["messages"][0]["id"]
            newer_messages = mc.download_newer_messages(group_id, newer_than_id, interval)

            #save to db
            if newer_messages != None:
                #merge newer_message to existed_messages
                self.my_db.update_group_messages(existed_messages, newer_messages, group_id)
                print("Messages data updated successfully.")
                return True
            else:
                print("No messages data updated.")
                return False
        else:
            self.pull_all_messages(group_id, interval)
    #################pull_newer_messages()#########################


    def pull_all_users(self, group_id, interval=5):
        mc = my_crawler.My_Crawler(group_id)
        dict_users = mc.download_all_users(group_id, interval)

        #save to db
        if dict_users != None:
            self.my_db.save_group_users(dict_users, group_id)
            return True
        else:
            return False
    ############pull_all_users()###############################


    def get_group_name(self, group_id):

        exsited_messages = self.my_db.get_group_messages(group_id)
        if exsited_messages == None:
            print("Group data is not exsited yet")
        else:
            return exsited_messages["meta"]["feed_name"]
    ########get_group_name###########################################


    def get_group_messages(self, group_id):

        exsited_messages = self.my_db.get_group_messages(group_id)
        #logic, algorithm

        return exsited_messages
    #############get_group_message()###############################


    def get_group_users(self, group_id):

        exsited_users = self.my_db.get_group_users(group_id)
        return exsited_users
    ########get_group_users()#####################################


    def get_user_info(self, user_id):

        existed_users = self.get_group_users(group_id)

        return



if __name__ == '__main__':

    print("start my_yammer")

    email_add = ''
    csl = ''
    pwd = ''

    my_yammer = My_Yammer()



    print("done")