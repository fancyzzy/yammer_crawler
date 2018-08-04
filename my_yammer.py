#!/usr/bin/env python2
#!encoding: utf-8

#import selenium
from selenium import webdriver
import time

import sys

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == '__main__':

    print("start")

    #profile
    #profile_dir = r'C:\Users\tarzonz\AppData\Roaming\Mozilla\Firefox\Profiles\e6k753v5.default'
    #profile = webdriver.FirefoxProfile(profile_dir)
    #wd = webdriver.Firefox(profile)
    #wd = webdriver.Firefox()
    wd = webdriver.Chrome()
    session_id = wd.session_id
    exe_url = wd.command_executor._url
    print("DEBUG session_id = {}, exe_url = {}".format(session_id, exe_url))
    print("DEBUG id(wd) = {}".format(id(wd)))


    url = r'https://www.baidu.com'
    #need to input email and then csl and cip
    ya_url = r'https://www.yammer.com/nokia.com/#/threads/inGroup?type=in_group&feedId=15273590'
    #need to firstly use the above url to login yammer
    jason_url = r'https://www.yammer.com/api/v1/messages/in_group/15273590.json'
    #wd.maximize_window()

    print("start open firefox")
    wd.get(ya_url)
    print("DEBUG wd.title: {}".format(wd.title))


    print("start login")
    login_email = wd.find_element_by_id("i0116")
    login_email.send_keys("felix.zhang@nokia-sbell.com")
    wd.find_element_by_id("idSIButton9").click()
    #js_str = r'setTimeout(function(){document.getElementById("idSIButton9").click()},100)'
    #wd.execute_script(js_str)


    #handles
    handles = wd.window_handles
    print("DEBUG handles: {}".format(handles))
    current_h = wd.current_window_handle
    print("DEBUG current_handle: {}".format(current_h))

    print("DEBUG start to wait")
    #wd.implicitly_wait(60)

    for i in range(10):
        print(i)
        time.sleep(1)
    print("DEBUG wait over")


    print("finish window")
    #wd.switch_to.window(current_window)
    #al = wd.switch_to_alert()
    #print("DEBUG al.text = {}".al.text)
    #al.send_keys("tarzonz")

    handles = wd.window_handles
    print("DEBUG handles: {}".format(handles))
    current_h = wd.current_window_handle
    print("DEBUG current_handle: {}".format(current_h))


    print("Debug, after wait, id(wd) = {}".format(id(wd)))
    ruan_url = "http://www.ruanyifeng.com/blog/"
    newwindow = r'window.open("{}");'.format(jason_url)
    #newwindow = r'window.open("{}");'.format(ruan_url)
    wd.execute_script(newwindow)

    handles = wd.window_handles
    wd.switch_to.window(handles[-1])

    print("wd.title: {}".format(wd.title))

    #t1 = wd.find_element_by_css_selector('div:')
    print("wd.page_source: {}".format(wd.page_source))
    print("\n")
    print("wd_page_source[-100:]: {}".format(wd.page_source[-100:]))

    handles = wd.window_handles
    current_h = wd.current_window_handle
    print("handles: {}".format(handles))
    print("current_handle: {}".format(current_h))



    print("done")