#!/usr/bin/env python


'''
Use matplotlib to draw  figures of  post and updates points
'''


import numpy as np
import os

#import matplotlib
#matplotlib.use('Agg')

SAVE_PATH = os.path.join(os.getcwd(),'static')

def draw_figure(data_list, threshold, date_end, date_start):
    '''

    :param data_list: [[id,name,updates,posts,photo],...]
    :param threshold: in fact it is no usage since the data_list has been filtered already
    :param date_end:
    :param date_start:
    :return:
    '''

    import matplotlib.pyplot as plt


    print("DEBUG start draw_figure")
    if date_start == None:
        date_start = "beginning"
    if date_end == None:
        date_end = "Now"
    post_list= [x[3] for x in data_list if x[2]>threshold or x[3]>threshold]
    comment_list = [x[2] for x in data_list if x[2]>threshold or x[3]>threshold]
    name_list = [x[1] for x in data_list if x[2]>threshold or x[3]>threshold]
    photo_list= [x[-1] for x in data_list if x[2]>threshold or x[3]>threshold]

    print("start color")
    color = np.arctan2(post_list, comment_list)
    #print("DEBUG color: {}".format(color))

    print("start plt.figure with plt id:{}".format(id(plt)))
    #fig= plt.figure(figsize=(8.0, 5.0))
    #Set fig size/resolution
    fig= plt.figure(figsize=(11.0, 7.5))

    print("start fig.add_subplot")
    ax1 = fig.add_subplot(111)


    title_str = "Comments and Posts from %s to %s"%(date_end, date_start)
    ax1.set_title(title_str)
    plt.ylabel("Post Number")
    plt.xlabel("Comment Number")
    max_y = 100
    max_x = 100
    if post_list:
        max_y = max(post_list)
    if comment_list:
        max_x = max(comment_list)

    plt.yticks([x for x in range(max_y + 20) if x % 5 == 0])
    plt.xticks([y for y in range(max_x + 20) if y % 5 == 0])
    plt.ylim(-10, max_y+10)
    plt.xlim(-10, max_x+10)

    print("Start to scatter")

    p_scatter = ax1.scatter(comment_list, post_list, s=155, c = color, alpha=0.5, marker='o', cmap=plt.get_cmap("Spectral"))

    labels = []
    for i in range(len(name_list)):

        label = (name_list[i] + "\n(%d,%d)"%(comment_list[i], post_list[i]))
        labels.append(label)

        plt.annotate(label,\
        xy=(comment_list[i], post_list[i]), xytext=(comment_list[i]+0.5, post_list[i]+0.1),\
        fontsize=8)

    #legend
    #ax1.legend(name_list, loc = 'top left', scatterpoints=1)
    #ax1.legend()

    #Delete right and top spines
    ax1.spines['top'].set_color('none')
    ax1.spines['right'].set_color('none')

    print("Return plt, id: {}".format(id(plt)))

    return plt
################draw_figure()##################################################################


if __name__ == '__main__':

    example_list = [[1639993032, u'LI Ellen', 54, 87, u'https://mug0.assets-yammer.com/mugshot/images/48x48/5h0BJ82WH7kQHlN3HJVbnrXTSMPBTfP1'],
[1639849062, u'MAI Maggie', 15, 24, u'https://mug0.assets-yammer.com/mugshot/images/48x48/nbJkD-pZVvtD9WmNlgHzRxmsDj83glHw'],
[1640337160, u'LIU Aaron', 7, 3, u'https://mug0.assets-yammer.com/mugshot/images/48x48/mbLFljlLhwkq2LttSJVn5C6TQpK01dnq'],
[1639911169, 'unknown user', 6, 1, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1639869576, u'LI Xin', 5, 31, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1642625168, u'LIU Albert', 5, 6, u'https://mug0.assets-yammer.com/mugshot/images/48x48/SQcJk93P3S8VWH6TSXSBTX2mfzN8QzC4'],
[1640005660, u'CHEN Chris', 4, 2, u'https://mug0.assets-yammer.com/mugshot/images/48x48/PrBm7gfNwNF5CgRrGpqgx8bP9wPJQMxq'],
[1610777031, u'XIE Crystal', 3, 4, u'https://mug0.assets-yammer.com/mugshot/images/48x48/hR45kTbX48WXnxJFK4JKDgXtKZ2hvRLq'],
[1640229078, u'YAN Tim', 3, 0, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1639997404, u'YANG Ellen', 3, 6, u'https://mug0.assets-yammer.com/mugshot/images/48x48/dHF8k13FKzdj3H8cxtGCt1GrtGfNNB0n'],
[1640229073, 'unknown user', 3, 3, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1568965136, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1641702550, u'ZHANG Vicky', 2, 10, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1606014178, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1538182089, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1540232816, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1640004140, u'ZHAO Joshua', 2, 0, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1569252594, 'unknown user', 1, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png']]




    threshold = 0
    date_start = None
    date_end = None
    plt =  draw_figure(example_list, threshold, date_end, date_start)
    #plt.show()
    #plt.savefig("test.png", dpi=200)

    print("Done")