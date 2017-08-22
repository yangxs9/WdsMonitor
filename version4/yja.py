# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5944#1',
    'group': 'SNH48-易嘉爱应援会',
    'qq': '155018267',
    'name': '嘉爱',
    'activity': 'SNH48-易嘉爱应援会第四届总选举微打赏',
    'slogan': '年夜饭的每一份心意对于守年来说都是非常重要的，2017年的这个夏天，一起为嘉爱的梦想之路加油吧！',
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
    msg += '目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
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

