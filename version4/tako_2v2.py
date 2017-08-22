# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 200

info0 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6045#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'Tako',
    'activity': '我们宣誓效忠【灵魂使徒张语格】',
    'slogan': '这个夏天为张语格而战，语归神七，格战到底！',
    'isTurnOn': True,
}

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6048#1',
    'group': '',
    'qq': '',
    'name': '消音',
    'activity': '',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6047#1',
    'group': '',
    'qq': '',
    'name': 'momo',
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

def sendMsg(mainWds, friendWds, other1, other2):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持！\n'
    msg += mainWds.activity + '正在进行中，目前情况：\n'
    
    msg += mainWds.name + '+' + friendWds.name + '：' 
    msg += str(mainWds.amount) + '+' + str(friendWds.amount) + '=' + str(round(mainWds.amount + friendWds.amount, 2)) + '\n'
    
    msg += other1.name + '+' + other2.name + '：' 
    msg += str(other1.amount) + '+' + str(other2.amount) + '=' + str(round(other1.amount + other2.amount, 2)) + '\n'
    
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan
    msg += '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds0 = Wds.Wds(info0)
wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)
wds3 = Wds.Wds(info3)

while True:
    time.sleep(interval)
    try:
        wds0.refreshInfo()
    except:
        print('refresh error')
    if wds0.isChanged:
        wds1.refreshInfo()
        wds2.refreshInfo()
        wds3.refreshInfo()
        sendMsg(wds0, wds1, wds2, wds3)
