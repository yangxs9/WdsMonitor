# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6015#1',
    'group': 'SNH48-於佳怡应援会',
    'qq': '467473456',
    'name': '小公主',
    'activity': '',
    'slogan': '建造於佳怡的城堡每一步都需要有你的支持，让我们一起为最可爱的小公主筑起心里最美的城堡，陪她看最美的风景！',
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

