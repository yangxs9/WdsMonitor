# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180
silence_interval = 10000.0

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6603#1',
    'group': 'BEJ48-刘胜男应援会',
    'qq': '548718867',
    'name': '小树',
    'activity': '小树的生诞众筹',
    'slogan': '一起为小树过个最棒的生日吧！',
    'isTurnOn': True,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def singleSend(mainWds):
    msg = 'biu biu biu～'
    for user in mainWds.addedUserMoney:
        msg += '感谢' + user + '刚刚支持了' + str(mainWds.addedUserMoney[user]) + '元！'
    msg += mainWds.activity + '正在进行中，目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
lastTime = time.time()

while True:
    time.sleep(interval)
    try:
        wds1.refreshInfo()
    except:
        print('refresh error')
    currentTime = time.time()
    if wds1.isChanged:
        singleSend(wds1)
        lastTime = currentTime

