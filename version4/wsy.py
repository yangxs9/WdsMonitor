# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5476#1',
    'group': 'SNH48-王偲越应援会',
    'qq': '480359869',
    'name': '菜菜',
    'activity': '',
    'slogan': '一个古典味十足的名字，配上一个可爱的脸蛋，加上精通二胡民族舞。现在，就需要你一份支持，使菜菜能在更好的环境成长，成长为一棵美丽而有营养的菜菜，一棵日后听到王偲越三字会使我们感到自豪的美菜。',
    'isTurnOn': True,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def singleSend(mainWds):
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + '刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持！\n'
    msg += '目前总额' + str(mainWds.amount) + '元，距离目标金额10000还差' + str(round(10000 - mainWds.amount,2)) + '元，参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)

while True:
    time.sleep(interval)
    try:
        wds1.refreshInfo()
    except:
        print('refresh error')
    if wds1.isChanged:
        singleSend(wds1)

