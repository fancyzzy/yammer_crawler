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
YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
#YAMMER_API_USER = 'https://www.yammer.com/api/v1/users/in_group/15273590.json'

YAMMER_API_USER = 'https://www.yammer.com/api/v1/users/in_group/'


def simulate_keyboard(the_str):
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys(the_str)


###############simulate_keyboard()########################



class My_Crawler():
    def __init__(self):
        # profile
        # profile_dir = r'C:\Users\tarzonz\AppData\Roaming\Mozilla\Firefox\Profiles\e6k753v5.default'
        # profile = webdriver.FirefoxProfile(profile_dir)
        #self.wd = webdriver.Firefox()
        self.my_browser = webdriver.Chrome()
        print("start open selenium, my_browser: {}".format(self.my_browser))
        print("DEBUG TRI: {}".format(TRIGGER_URL))
        self.my_browser.get(TRIGGER_URL)
        print("DEBUG wd.title: {}".format(self.my_browser.title))

        #login
        print("start login")
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


        print("Login successful!")




    def download_all(self):
        pass

    def download(self):
        pass




if __name__ == '__main__':
    my_crawler = My_Crawler()




