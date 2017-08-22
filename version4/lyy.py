# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5685#1',
    'group': 'BEJ48-李媛媛应援会',
    'qq': '557263644',
    'name': '布丁',
    'activity': 'BEJ48-李媛媛 第四届总决选日常打卡第三期',
    'slogan': '',
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
    msg = 'Yummy，yummy！'
    for user in mainWds.addedUserMoney:
        msg += '感谢' + user + ' 在总选集资中为布丁投下了' + str(mainWds.addedUserMoney[user]) + '个媛份！'
    msg += '一起为布丁加油鼓劲吧。\n'
    msg += '总选淘宝：http://c.b1yt.com/h.8Vanlr?cv=1TarZDISlbn&sm=804200\n微打赏链接：https://wds.modian.com/show_weidashang_pro/5685#1'
    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)

while True:
    time.sleep(interval)
    try:
        wds1.refreshInfo()
    except:
        print('refresh error')
    if wds1.isTurnOn and wds1.isChanged:
        singleSend(wds1)

