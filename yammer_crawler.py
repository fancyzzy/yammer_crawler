#!/usr/bin/env python2


import  urllib2


def download(url, user_agent='wswp', num_retries=2):
    print("downloading: {}".format(url))
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print("Download error: {}".format(e.reason))
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries-1)
    return html



if __name__ == '__main__':
    url = 'https://www.yammer.com/nokia.com/#/threads/inGroup?type=in_group&feedId=15273590&view=all'
    url = 'https://www.yammer.com/api/v1/messages/in_group/15273590.json'
    #url = 'http://directory.app.alcatel-lucent.com/en/Rupi=CV0028763'
    #url = 'http://directory.app.alcatel-lucent.com/en/Lupi=CV0028763'

    html = download(url)
    print("DEBUG html: {}".format(html))
