#!/usr/bin/env python

'''
Crawl yammer message info
by RESful API:
https://www.yammer.com/api/v1/messages/in_group/15273590.json

Method:
Use yampy to download json data
'''

from bs4 import BeautifulSoup
import json
import yampy
import time



BASE_API = 'http://www.yammer.com/api/v1'
#YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/15273590.json'
YAMMER_GROUP_MESSAGES = 'https://www.yammer.com/api/v1/messages/in_group/'
#YAMMER_API_USER = 'https://www.yammer.com/api/v1/users/in_group/15273590.json'

YAMMER_GROUP_USERS = 'https://www.yammer.com/api/v1/users/in_group/'

API_RESTRICT = 20

MY_CLIENT_ID = '2fxbPxiDYwtM40yN3m0fQ'
MY_CLIENT_SECRET = 'hJKivZUnqsl6vAP2NyaFodWK2nNDxHJ5MxwPtg4s'
REDIRECT_URI = 'https://yammerstate.herokuapp.com'


def extend_diff(list_source, list_new):
    for item in list_new:
        if item not in list_source:
            list_source.append(item)
###############extend_diff()#############################

from types import  MethodType
def from_group(self, group_id, older_than=None, newer_than=None,
               limit=None, threaded=None):
    """
    Returns messages that were posted in the group identified by group_id.

    See the :meth:`all` method for a description of the keyword arguments.
    """
    path = "/messages/in_group/%d" % (group_id)
    return self._client.get(path, **self._argument_converter(
        older_than=older_than,
        newer_than=newer_than,
        limit=limit,
        threaded=threaded,
        ))


class My_Crawler():
    def __init__(self, access_token=None):

        '''
        authenticator = yampy.Authenticator(client_id=MY_CLIENT_ID, client_secret=MY_CLIENT_SECRET)
        auth_url = authenticator.authorization_url(redirect_uri=REDIRECT_URI)
        print("Debug auth_url: {}".format(auth_url))

        auth_url = \
        'https://www.yammer.com/dialog/oauth?client_id=2fxbPxiDYwtM40yN3m0fQ&redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'

        code = "xMK0kj1bGHmCp6gELwX44Q"

        access_data = authenticator.fetch_access_data(code)

        access_token = access_data.access_token.token
        print("DEBUG access_token: {}".format(access_token))
        '''

        if access_token == None:
            print("DEBUG token = None")
            return

        self.yampy = yampy.Yammer(access_token=access_token)

        #dynamicly add method
        self.yampy.messages.from_group = MethodType(from_group, self.yampy.messages)

        print("Init finished")

    ############__init__()##############


    def get_group_name(self, group_id):
        '''
        get group name from the message dict
        :param group_id:
        :return:
        '''

        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id)
        print("Check group name in 'meta','feed_name' of {}".format(group_messages_url))

        # Call yampy API
        json_dict = self.yampy.messages.from_group(group_id)

        if json_dict != None:
            group_name = json_dict["meta"]["feed_name"]
            return group_name
        else:
            return None
    ##########get_group_name()#####################


    def mdownload_all_messages(self, group_id, interval=5, older_than_message_id=None, n=None):
        '''

        download all the messages in the group
        continue to download until no new messages
        as one time only 20 messages allowed
        :param group_id: string, yammer group id
        :param interval: download interval
        :param older_than_message_id: only download older messages than this
        :param n: download times
        :return: json liked dict
        '''

        print("Start download all messages")
        json_result = None
        json_str = None
        i = 0
        #YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id)
        if older_than_message_id != None:
            group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?older_than=%s'%(older_than_message_id)

        while 1:
            i += 1
            print("Download batch {}".format(i))
            print("url: {}".format(group_messages_url))

            #Call yampy API
            json_dict = self.yampy.messages.from_group(group_id, older_than_message_id)

            print("DEBUG type(json_dict): {}".format(type(json_dict)))
            print("DEBUG json_dict: {}".format(json_dict))

            #concatenate json_str to json_result
            if json_result == None:
                json_result = json_dict
            else:
                if "messages" in json_dict.keys():
                    json_result["messages"].extend(json_dict["messages"])
                else:
                    print("Error, there is no message key!")
                    break

                if "feferences" in json_dict.keys():
                    extend_diff(json_result["references"], json_dict["references"])
                if "followed_user_ids" in json_dict["meta"].keys():
                    extend_diff(json_result["meta"]["followed_user_ids"], json_dict["meta"]["followed_user_ids"])
                if "followed_references" in json_dict["meta"].keys():
                    extend_diff(json_result["meta"]["followed_references"], json_dict["meta"]["followed_references"])

            # Check to continue
            if json_dict["meta"]["older_available"]:
                print("older available, sleep %d second.."%(interval))
                time.sleep(interval)
                older_than_message_id = json_dict["messages"][-1]["id"]
                group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + \
                                     '?older_than=%s'%(older_than_message_id)
            else:
                print("No more messages, download finished")
                break

            if n and i >= n:
                print("Stop download by %d times"%(n))
                break

        return json_result

    ###########download_all_messages()###################################################


    def download_newer_messages(self, group_id, newer_than_message_id, interval=5):
        '''
        Download newer messages based on the existing database

        :param group_id:
        :param newer_than_message_id:
        :return: newer_json_result
        '''

        print("Start download newer messages than %s"%(newer_than_message_id))
        newer_json_result = None
        json_str = None
        i = 0
        #YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?newer_than=%s'%(newer_than_message_id)

        older_than_message_id = None

        while 1:
            i += 1
            print("Download batch {}".format(i))
            print("url: {}".format(group_messages_url))

            #Call yampy API
            if not older_than_message_id:
                json_dict = self.yampy.messages.from_group(group_id, None, newer_than_message_id)
            else:
                json_dict = self.yampy.messages.from_group(group_id, older_than_message_id)

            #print("DEBUG json_dict: {}".format(json_dict))
            if len(json_dict["messages"]) == 0:
                print("No new messages found.")
                break

            #concatenate json_str to newer_json_result
            if newer_json_result == None:
                newer_json_result = json_dict
            else:
                #May have same messages
                extend_diff(newer_json_result["messages"], json_dict["messages"])

                extend_diff(newer_json_result["references"], json_dict["references"])
                extend_diff(newer_json_result["meta"]["followed_user_ids"],\
                            json_dict["meta"]["followed_user_ids"])
                extend_diff(newer_json_result["meta"]["followed_references"],\
                            json_dict["meta"]["followed_references"])

            # Check to stop, if < 20 means download complete
            if len(json_dict["messages"]) < API_RESTRICT:
                print("No more newer messages, download finished")
                break
            else:
                for message_dict in json_dict["messages"]:
                    if message_dict["id"] == newer_than_message_id:
                        print("No more newer messages, download finished")
                        break

            print("more newer messages available, sleep %d second.."%(interval))
            time.sleep(interval)
            older_than_message_id = json_dict["messages"][-1]["id"]
            group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + \
                                 '?older_than=%s'%(older_than_message_id)

        return newer_json_result
    ###########################download_newer_messages()##########################################


    def get_latest_message(self, group_id, json_data):
        '''
        :param group_id:
        :param json_data:
        :return: message_id str
        '''
        message_id = ''

        return json_data["messages"][0]["id"]
    ##########get_latest_message#########################################################


    def get_oldest_message(self, group_id, json_data):
        '''
        :param group_id:
        :param json_data:
        :return: message_id str
        '''
        message_id = ''

        return json_data["messages"][-1]["id"]
    #############get_oldest_message()####################################################


    def download_all_users(self, group_id, interval=5):
        '''

        download all the users in the group
        :param group_id: string, yammer group id
        :param interval: download interval
        :return: json liked dict see:
        https://www.yammer.com/api/v1/users/in_group/15273590.json
        '''
        print("Start download all users")

        json_result = None
        json_str = None
        i = 0
        page_num = 0
        #YAMMER_GROUP_USER = 'https://www.yammer.com/api/v1/users/in_group/'
        group_users_url = YAMMER_GROUP_USERS  + '%s.json'%(group_id)

        while 1:
            i += 1
            print("Download batch {}".format(i))
            print("url: {}".format(group_users_url))

            #Call yampy API
            json_dict = self.yampy.users.in_group(group_id, page_num)

            #concatenate json_str to json_result
            if json_result == None:
                json_result = json_dict
            else:
                if len(json_dict["users"]) != 0:
                    json_result["users"].extend(json_dict["users"])

                    extend_diff(json_result["meta"]["followed_user_ids"], json_dict["meta"]["followed_user_ids"])
                else:
                    print("Can't find more users due to yammer api bug")
                    break

            # Check to continue
            if json_dict["more_available"]:
                print("more available, sleep %d second.."%(interval))
                time.sleep(interval)

                page_num = i+1
                group_users_url = YAMMER_GROUP_USERS + '%s.json'%(group_id) + '?page=%d'%(page_num)
            else:
                print("No more users, download finished")
                break

        return json_result

    ###########download_all_users()###################################################


    def download_user_details(self, user_dict, interval=5):
        '''
        download one user detailed information from a exsited user dict

        :param user_dict: Contatins all user info in key 'url' value
        see: https://www.yammer.com/api/v1/users/1640338967.json
        :return: details of all users in this group as json files for each user
        '''

        full_name = ''
        job_title = ''
        state = '' #if this id is still available
        user_url = user_dict["url"] + '.json'
        user_name = user_dict["full_name"]
        print("Start download user detail of {}".format(user_name))
        print("url: {}".format(user_url))
        json_str = None

        '''
        js_cmd = r'window.open("{}");'.format(user_url)
        self.my_browser.execute_script(js_cmd)

        # handles
        handles = self.my_browser.window_handles
        self.my_browser.switch_to.window(handles[-1])
        current_h = self.my_browser.current_window_handle

        soup = BeautifulSoup(self.my_browser.page_source, features="html.parser")
        json_str = soup.get_text("body")
        '''

        # Convert to python dict from a json like string
        json_dict = json.loads(json_str)

        # close this window tag
        self.my_browser.close()
        handles = self.my_browser.window_handles
        self.my_browser.switch_to.window(handles[0])

        sleep(interval)
        return json_dict

    ###########download_all_user_details()############################################


if __name__ == '__main__':

    group_id = 15273590
    access_token = '592-FnmLDb1cF0zMgyj32jnz0w'
    my_crawler = My_Crawler(access_token)

    '''
    #test download and save all messages in the group
    result_json = my_crawler.download_all_messages(group_id, interval=1, older_than_message_id=None, n=None)
    print("Debug messages number: {}, result_json: {}".format(len(result_json["messages"]), result_json))
    file_name = 'group_%s_messages.json'%(group_id)
    with open(file_name, 'w') as fb:
        #convert dict to string
        fb.write(json.dumps(result_json))
    '''


    '''
    #test download and save all users in the group
    
    #group_id = 12562314 #QD Center
    group_id = 15273590 #GSM English Group
    result_json = my_crawler.download_all_users(group_id, interval=1)
    print("Debug users number: {}, result_json: {}".format(len(result_json["users"]), result_json))
    file_name = 'group_%s_users.json'%(group_id)
    with open(file_name, 'w') as fb:
        fb.write(json.dumps(result_json))
    '''


    #Test to download newer messages
    newer_than_message_id = '1147793449'
    newer_result_json = my_crawler.download_newer_messages(group_id, newer_than_message_id, interval=1)
    if newer_result_json:
        print("DEBUG new message num: {}, newer_result_json: {}".\
     format(len(newer_result_json["messages"]), newer_result_json))
    else:
        print("None newer messages")

    print("done")




