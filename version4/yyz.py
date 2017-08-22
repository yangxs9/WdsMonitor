# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4956#1',
    'group': '袁雨桢应援会',
    'qq': '',
    'name': '余震',
    'activity': '【【袁雨桢篇】天王山圣杯争夺战-微打赏】',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4959#1',
    'group': '杨惠婷应援会',
    'qq': '',
    'name': '杨惠婷',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

info3 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4955#1',
    'group': '杨冰怡应援会',
    'qq': '',
    'name': '杨冰怡',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def lastGroup(wdss):
    minAmount = 9000000.0
    lastGroup = ''
    for wds in wdss:
        if wds.amount < minAmount:
            minAmount = wds.amount
            lastGroup = wds.group
    return lastGroup

def sendMsg(mainWds, others):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += '@' + user + ' 刚刚在' + mainWds.activity + '打赏了' + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢这位聚聚！给你笔芯哦！\n'
    msg += '目前已筹集金额：' + str(mainWds.amount) + '元。\n'
    msg += '★当前对手家应援会的集资情况为：\n'
    for otherWds in others:
        msg += '·' + otherWds.group + '：' + str(otherWds.amount) + '元\n'
    msg += lastGroup([mainWds] + others) + '暂时落后。\n'
    msg += '微打赏地址：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)
wds3 = Wds.Wds(info3)

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    if wds1.isTurnOn and wds1.isChanged:
        wds2.refreshInfo()
        wds3.refreshInfo()
        sendMsg(wds1, [wds2, wds3])
