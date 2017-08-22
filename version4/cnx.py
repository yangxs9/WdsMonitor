# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6286#1',
    'group': 'GNZ48-陈楠茜应援群',
    'qq': '550562023',
    'name': 'Nancy',
    'activity': '',
    'slogan': '谢谢你为陈楠茜的梦想而努力 2017的盛夏，一起来为成为她的羽翼让她破茧成蝶而奋斗吧！',
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

