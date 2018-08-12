#!/usr/bin/env python


'''
Use matplotlib to draw  figures of  post and updates points
'''

import matplotlib.pyplot as plt
import numpy as np




if __name__ == '__main__':

    example_list = [[1639993032, u'LI Ellen', 141, 87, u'https://mug0.assets-yammer.com/mugshot/images/48x48/5h0BJ82WH7kQHlN3HJVbnrXTSMPBTfP1'],
[1639849062, u'MAI Maggie', 39, 24, u'https://mug0.assets-yammer.com/mugshot/images/48x48/nbJkD-pZVvtD9WmNlgHzRxmsDj83glHw'],
[1639869576, u'LI Xin', 36, 31, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1639997752, u'LI Hui', 36, 35, u'https://mug0.assets-yammer.com/mugshot/images/48x48/MqF14SXQ9mlm1wtKc80dZ32hJlKbdV0b'],
[1540220095, u'ZHOU Ron', 15, 14, u'https://mug0.assets-yammer.com/mugshot/images/48x48/2Nq-KH4qCKjLjjlmhq7rvrdjRd2Z-FGN'],
[1641702550, u'ZHANG Vicky', 12, 10, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1642625168, u'LIU Albert', 11, 6, u'https://mug0.assets-yammer.com/mugshot/images/48x48/SQcJk93P3S8VWH6TSXSBTX2mfzN8QzC4'],
[1640337160, u'LIU Aaron', 10, 3, u'https://mug0.assets-yammer.com/mugshot/images/48x48/mbLFljlLhwkq2LttSJVn5C6TQpK01dnq'],
[1576812066, u'LUO Turing', 9, 8, u'https://mug0.assets-yammer.com/mugshot/images/48x48/wbNBkQ3Z5qWPhQdJ9Tkwdb0WNpTrG98s'],
[1639997404, u'YANG Ellen', 9, 6, u'https://mug0.assets-yammer.com/mugshot/images/48x48/dHF8k13FKzdj3H8cxtGCt1GrtGfNNB0n'],
[1639911169, 'unknown user', 7, 1, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1610777031, u'XIE Crystal', 7, 4, u'https://mug0.assets-yammer.com/mugshot/images/48x48/hR45kTbX48WXnxJFK4JKDgXtKZ2hvRLq']]

    threshold = 0
    date_start = None
    date_end = None
    if date_start == None:
        date_start = "beginning"
    if date_end == None:
        date_end = "Now"
    post_list= [x[3] for x in example_list if x[2]>threshold or x[3]>threshold]
    comment_list = [x[2] for x in example_list if x[2]>threshold or x[3]>threshold]
    name_list = [x[1] for x in example_list if x[2]>threshold or x[3]>threshold]
    photo_list= [x[-1] for x in example_list if x[2]>threshold or x[3]>threshold]

    color = np.arctan2(comment_list, post_list)

    fig= plt.figure()
    ax1 = fig.add_subplot(111)

    title_str = "Comments and Posts from %s to %s"%(date_end, date_start)
    ax1.set_title(title_str)
    plt.xlabel("Posts")
    plt.ylabel("Comments")
    plt.xticks([x for x in range(max(post_list) + 20) if x % 10 == 0])
    plt.yticks([y for y in range(max(comment_list) + 20) if y % 10 == 0])
    ax1.scatter(post_list, comment_list,s=175, c = color, alpha=0.5, marker='o')
    ax1.colorbar()

    for i in range(len(name_list)):
        plt.annotate((name_list[i]+"\n(%d,%d)"%(post_list[i],comment_list[i])),\
                     xy=(post_list[i], comment_list[i]), xytext=(post_list[i]+0.5, comment_list[i]+0.1),\
                     fontsize=8)

    plt.show()

    print("Done")