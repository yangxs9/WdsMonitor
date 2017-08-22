# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 60

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5078#1',
    'group': 'SNH48-孔肖吟应援会',
    'qq': '221771881',
    'name': '小孔',
    'activity': '东北欢乐斗地主',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5077#1',
    'group': '',
    'qq': '',
    'name': '冯薪朵',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

info3 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5079#1',
    'group': '',
    'qq': '',
    'name': '孙芮',
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
    msg += mainWds.activity + '微打赏正在进行中，目前情况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    for otherWds in others:
        msg += otherWds.name + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += '微打赏链接：' + mainWds.url

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
