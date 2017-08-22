# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5617#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'Tako',
    'activity': '张语格四选众筹-第四弹 《前进一步 重回神七》',
    'slogan': '我们与神七的距离，需要你们，万分恳切的需要你们的支持！孤注一掷让张语格回神七！！丸子清仓吧！！',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6448#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'Tako',
    'activity': '',
    'slogan': '张语格总选倒计时，每日清仓，重回神七，不留遗憾！',
    'isTurnOn': True,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def singleSend(mainWds):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + '刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家对支持！\n'
    msg += '目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)


# wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)

while True:
    time.sleep(interval)
    # wds1.refreshInfo()
    # if wds1.isTurnOn and wds1.isChanged:
    #     singleSend(wds1)
    try:
        wds2.refreshInfo()
    except:
        print('refresh error')
    if wds2.isTurnOn and wds2.isChanged:
        singleSend(wds2)

