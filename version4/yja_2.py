# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6230#1',
    'group': 'SNH48-易嘉爱应援会',
    'qq': '155018267',
    'name': '女饭',
    'activity': '男饭女饭PK',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/6231#1',
    'group': '易嘉爱应援会',
    'qq': '155018267',
    'name': '男饭',
    'activity': '男饭女饭PK',
    'slogan': '',
    'isTurnOn': True,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)

def sendMsg(mainWds, otherWds):
    msg = ''
    if mainWds.isChanged:
        for user in mainWds.addedUserMoney:
            msg += user + ' 刚刚支持了嘉爱' + str(mainWds.addedUserMoney[user]) + '元，'       
    if otherWds.isChanged:
        for user in otherWds.addedUserMoney:
            msg += user + ' 刚刚支持了嘉爱' + str(otherWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持！\n'
    msg += mainWds.activity + '正在进行中，目前情况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    msg += otherWds.name + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += '女饭链接：' + mainWds.url + '\n'
    msg += '男饭链接：' + otherWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    wds2.refreshInfo()
    if wds1.isChanged or wds2.isChanged:
        sendMsg(wds1, wds2)
