#!/usr/bin/env python
from selenium import webdriver


if __name__ == '__main__':

    print("start")
    session_id = r'450c84d1b9c23d0e80488e4d99897e70'
    exe_url = r'http://127.0.0.1:64868'
    #dr = webdriver.Firefox()
    #dr = webdriver.Remote(command_executor=exe_url, desired_capabilities={})
    dr = webdriver.ReuseChrome(command_executor=exe_url, session_id=session_id)
    #dr.session_id = session_id
    print("opened")
    print(dr.current_url)

    jason_url = r'https://www.yammer.com/api/v1/messages/in_group/15273590.json'
    dr.get(jason_url)

    print("done")
