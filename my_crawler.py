#!/usr/bin/env python

'''
Crawl yammer message info
by RESful API:
https://www.yammer.com/api/v1/messages/in_group/15273590.json

Method:
Use selenium to simulate human operation
to bypass yammer authentication
'''

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import json

#Simulate keyboard input
import win32com.client as comclt
'''
wsh.SendKeys("abc") #types out abc directly into wherever you have your cursor (ex: right into this editor itself!)
wsh.SendKeys("{NUMLOCK}{CAPSLOCK}{SCROLLLOCK}")
'''

#Trigger to login
TRIGGER_URL = 'https://www.yammer.com/nokia.com/#/threads/inGroup?type=in_group&feedId=15273590'
LOGIN_EMAIL = 'felix.zhang@nokia-sbell.com'
LOGIN_CSL = 'tarzonz\t'
LOGIN_PWD = 'CV_28763_14a\r'

#YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/15273590.json'
YAMMER_GROUP_MESSAGES = 'https://www.yammer.com/api/v1/messages/in_group/'
#YAMMER_API_USER = 'https://www.yammer.com/api/v1/users/in_group/15273590.json'

YAMMER_GROUP_USERS = 'https://www.yammer.com/api/v1/users/in_group/'
API_RESTRICT = 20


def simulate_keyboard(the_str):
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys(the_str)
###############simulate_keyboard()########################


def extend_diff(list_source, list_new):
    for item in list_new:
        if item not in list_source:
            list_source.append(item)
###############extend_diff()#############################



class My_Crawler():
    def __init__(self, group_id):
        # profile
        # profile_dir = r'C:\Users\tarzonz\AppData\Roaming\Mozilla\Firefox\Profiles\e6k753v5.default'
        # profile = webdriver.FirefoxProfile(profile_dir)
        #self.wd = webdriver.Firefox()
        self.my_browser = webdriver.Chrome()
        print("Created my_browser: {}".format(self.my_browser))

        self.login_ok = False
        self.trigger_login(group_id)

        #self.my_parser = my_parser.My_Parser()
        #self.my_database = my_database.My_Database()
    ############__init__()##############


    def is_login_ok(self):
        return self.login_ok
    ##########is_login_ok()#############


    def quit(self):
        self.my_browser.quit()
    ###############quit()###############


    def trigger_login(self, group_id):
        '''
        Simulate human operation to login
        by selenium
        :return:
        '''
        #login
        print("start login")
        print("TRIGGER login url: {}".format(TRIGGER_URL))
        self.my_browser.get(TRIGGER_URL)

        login_email = self.my_browser.find_element_by_id("i0116")
        login_email.send_keys(LOGIN_EMAIL)
        self.my_browser.find_element_by_id("idSIButton9").click()
        #javascript style click
        # js_str = r'setTimeout(function(){document.getElementById("idSIButton9").click()},100)'
        # self.my_browser.execute_script(js_str)
        for i in range(10):
            print(i)
            sleep(1)

        #Simulate keyboard press:
        simulate_keyboard(LOGIN_CSL+LOGIN_PWD)

        #here is a timer to denfend hanging loggin

        self.group_name = self.get_group_name(group_id)
        if self.group_name:
            print("login %s successful"%(self.group_name))
            self.login_ok = True
        else:
            print("login failed!")
    ############trigger_login()###################

    def get_group_name(self, group_id):

        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id)

        js_cmd = r'window.open("{}");'.format(group_messages_url)
        self.my_browser.execute_script(js_cmd)

        handles = self.my_browser.window_handles
        self.my_browser.switch_to.window(handles[-1])

        soup = BeautifulSoup(self.my_browser.page_source, features="html.parser")

        json_str = soup.get_text("body")
        json_dict = json.loads(json_str)

        group_name = json_dict["meta"]["feed_name"]

        return group_name
    ##########get_group_name()#####################


    def download_all_messages(self, group_id, interval=5, older_than_message_id=None, n=None):
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
        soup = None
        #YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id)
        if older_than_message_id != None:
            group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?older_than=%s'%(older_than_message_id)


        while 1:
            i += 1
            print("Download batch {}".format(i))
            print("url: {}".format(group_messages_url))

            js_cmd = r'window.open("{}");'.format(group_messages_url)
            self.my_browser.execute_script(js_cmd)

            # handles
            handles = self.my_browser.window_handles
            self.my_browser.switch_to.window(handles[-1])
            current_h = self.my_browser.current_window_handle
            #print("DEBUG handles: {}, current_handle: {}".format(handles, current_h))

            soup = BeautifulSoup(self.my_browser.page_source, features="html.parser")
            json_str = soup.get_text("body")
            # Get all the text contents from the page
            # html = self.browser.page_source
            # print("DEBUG soup.body: {}".format(soup.body))
            # print("DEBUG json_str: {}".format(json_str))

            # Or you can just designate to the only block content
            # json_str = soup.pre.contents[0]

            # Convert to python dict from a json like string
            json_dict = json.loads(json_str)
            #print("DEBUG json_dict['meta']['older_available'] = {}".format(json_dict["meta"]["older_available"]))
            #print("DEBUG len(json_dict['messages']): {}".format(len(json_dict['messages'])))
            #print("DEBUG json_dict['messages'][-1]: {}, json_dict['messages'][-1]['id']: {}". \
            #    format(json_dict['messages'][-1], json_dict['messages'][-1]['id']))


            #concatenate json_str to json_result
            if json_result == None:
                json_result = json_dict
            else:
                if len(json_dict["messages"]) != 0:
                    json_result["messages"].extend(json_dict["messages"])

                    extend_diff(json_result["references"], json_dict["references"])
                    extend_diff(json_result["meta"]["followed_user_ids"], json_dict["meta"]["followed_user_ids"])
                    extend_diff(json_result["meta"]["followed_references"], json_dict["meta"]["followed_references"])
                else:
                    print("Can't find more messages due to yammer api bug")
                    break

            # Check to continue
            if json_dict["meta"]["older_available"]:
                print("older available, sleep %d second.."%(interval))
                sleep(interval)
                last_message_id = json_dict["messages"][-1]["id"]
                print("continue to download older messages than id: %s."%(last_message_id))
                #print("DEBUG json_dict['messages'][-1]: {}, json_dict['messages'][-1]['id']: {}". \
                #    format(json_dict['messages'][-1], json_dict['messages'][-1]['id']))
                group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?older_than=%s'%(last_message_id)
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
        soup = None
        #YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?newer_than=%s'%(newer_than_message_id)

        while 1:
            i += 1
            print("Download batch {}".format(i))
            print("url: {}".format(group_messages_url))

            js_cmd = r'window.open("{}");'.format(group_messages_url)
            self.my_browser.execute_script(js_cmd)

            handles = self.my_browser.window_handles
            self.my_browser.switch_to.window(handles[-1])

            soup = BeautifulSoup(self.my_browser.page_source, features="html.parser")
            json_str = soup.get_text("body")
            json_dict = json.loads(json_str)

            #print("DEBUG json_dict: {}".format(json_dict))
            if len(json_dict["messages"]) == 0:
                print("No new messages so far")
                break

            #concatenate json_str to newer_json_result
            if newer_json_result == None:
                newer_json_result = json_dict
            else:
                if len(json_dict["messages"]) != 0:
                    #May have same messages
                    extend_diff(newer_json_result["messages"], json_dict["messages"])

                    extend_diff(newer_json_result["references"], json_dict["references"])
                    extend_diff(newer_json_result["meta"]["followed_user_ids"],\
                                json_dict["meta"]["followed_user_ids"])
                    extend_diff(newer_json_result["meta"]["followed_references"],\
                                json_dict["meta"]["followed_references"])
                else:
                    print("Can't find more messages due to yammer api bug")
                    break

            # Check to stop
            if "older_available" not in json_dict["meta"].keys():
                if len(json_dict["messages"]) < API_RESTRICT:
                    print("No more newer messages, download finished")
                    break
                else:
                    for message_dict in json_dict["messages"]:
                        if message_dict["id"] == newer_than_message_id:
                            print("Finding is over since newer_than_message_id got")
                            break

            else:
                if not json_dict["meta"]["older_available"]:
                    print("No more messages, download finished, this shuold not happen")
                    break
                else:
                    for message_dict in json_dict["messages"]:
                        if message_dict["id"] == newer_than_message_id:
                            print("Finding is over since newer_than_message_id got")
                            break


            print("more newer messages available, sleep %d second.."%(interval))
            sleep(interval)
            last_message_id = json_dict["messages"][-1]["id"]
            print("continue to download older messages than id: %s."%(last_message_id))
            group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?older_than=%s'%(last_message_id)

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
        :return: json liked dict
        '''
        print("Start download all users")

        json_result = None
        json_str = None
        i = 0
        page_num = 0
        soup = None
        #YAMMER_GROUP_USER = 'https://www.yammer.com/api/v1/users/in_group/'
        group_users_url = YAMMER_GROUP_USERS  + '%s.json'%(group_id)

        while 1:
            i += 1
            print("Download batch {}".format(i))
            print("url: {}".format(group_users_url))

            js_cmd = r'window.open("{}");'.format(group_users_url)
            self.my_browser.execute_script(js_cmd)

            # handles
            handles = self.my_browser.window_handles
            self.my_browser.switch_to.window(handles[-1])
            current_h = self.my_browser.current_window_handle

            soup = BeautifulSoup(self.my_browser.page_source, features="html.parser")
            json_str = soup.get_text("body")

            # Convert to python dict from a json like string
            json_dict = json.loads(json_str)

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
                sleep(interval)

                page_num = i+1
                group_users_url = YAMMER_GROUP_USERS + '%s.json'%(group_id) + '?page=%d'%(page_num)
            else:
                print("No more users, download finished")
                break

        return json_result

    ###########download_all_users()###################################################


    def download_messages_in_conversation(self, thread_id):
        '''
        Extract all the messages in a conversation
        if you are interested in this
        :param thread_id:
        :return:
        '''
        pass



if __name__ == '__main__':

    group_id = '15273590'
    my_crawler = My_Crawler(group_id)

    '''
    #download and save all messages in the group
    result_json = my_crawler.download_all_messages(group_id, interval=5, older_than_message_id=None, n=None)
    print("Debug messages result_json: {}".format(result_json))
    file_name = 'group_%s_messages.json'%(group_id)
    with open(file_name, 'w') as fb:
        #convert dict to string
        fb.write(json.dumps(result_json))
    '''


    '''
    group_id = '12562314' #QD Center
    #download and save all users in the group
    result_json = my_crawler.download_all_users(group_id, interval=5)
    print("Debug users result_json: {}".format(result_json))
    file_name = 'group_%s_users.json'%(group_id)
    with open(file_name, 'w') as fb:
        fb.write(json.dumps(result_json))
    '''


    #Test to download newer messages
    newer_than_message_id = '1126445002'
    newer_result_json = my_crawler.download_newer_messages(group_id, newer_than_message_id, interval=5)
    print("DEBUG newer_result_json: {}".format(newer_result_json))

    print("done")
    my_crawler.quit()




