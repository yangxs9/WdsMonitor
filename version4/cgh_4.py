# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6082#1',
    'group': 'SNH48-陈观慧应援会',
    'qq': '130594899',
    'name': '小艾',
    'activity': '艾斯嘉学院争霸赛',
    'slogan': '',
    'isTurnOn': True,
}

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6079#1',
    'group': '',
    'qq': '',
    'name': 'kiki',
    'activity': '',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6080#1',
    'group': '',
    'qq': '',
    'name': '震震',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

info3 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6081#1',
    'group': '',
    'qq': '',
    'name': '教练',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)

def sendMsg(mainWds, other1, other2, other3):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持！\n'
    msg += mainWds.activity + '正在进行中，目前各家情况：\n'
    
    msg += mainWds.name + '：' + str(mainWds.amount) + '元，' + str(mainWds.peopleNum) + '人参加\n'
    msg += other1.name + '：' + str(other1.amount) + '元，' + str(other1.peopleNum) + '人参加\n'
    msg += other2.name + '：' + str(other2.amount) + '元，' + str(other2.peopleNum) + '人参加\n'
    msg += other3.name + '：' + str(other3.amount) + '元，' + str(other3.peopleNum) + '人参加\n'
    
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
