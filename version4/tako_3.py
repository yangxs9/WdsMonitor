# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info0 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6294#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'Tako',
    'activity': '夏日抢盘大作战',
    'slogan': '这个夏天为张语格而战，语归神七，格战到底！',
    'isTurnOn': True,
}

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6295#1',
    'group': '',
    'qq': '',
    'name': '络络',
    'activity': '',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6296#1',
    'group': '',
    'qq': '',
    'name': '余震',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

info3 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6046#1',
    'group': '',
    'qq': '',
    'name': '毛毛',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)

def sendMsg(mainWds, others):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持！\n'
    msg += mainWds.activity + '正在进行中，目前情况：\n'
    
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    for otherWds in others:
        msg += otherWds.name + '：' + str(otherWds.amount) + ' * 2 = ' + str(round(otherWds.amount * 2, 2)) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'

    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan
    msg += '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds0 = Wds.Wds(info0)
wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)

while True:
    time.sleep(interval)
    try:
        wds0.refreshInfo()
    except:
        print('refresh error')
    if wds0.isChanged:
        wds1.refreshInfo()
        wds2.refreshInfo()
        sendMsg(wds0, [wds1, wds2])
