# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 60

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4813#1',
    'group': 'SNH48-孔肖吟应援会',
    'qq': '',
    'name': '小孔',
    'slogan': '音符们的每一份心意对于小孔来说都是非常重要的，今年这个夏天，让我们不留遗憾，冲击选拔！！',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4814#1',
    'group': 'SNH48-宜家爱应援会',
    'qq': '',
    'name': '嘉爱',
    'slogan': '',
    'isTurnOn': False,
}

info3 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4813#1',
    'group': 'SNH48-孔肖吟应援会',
    'qq': '',
    'name': '小孔',
    'slogan': '音符们的每一份心意对于小孔来说都是非常重要的，今年这个夏天，让我们不留遗憾，冲击选拔！！',
    'isTurnOn': True,
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
    msg += '目前战况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    for otherWds in others:
        msg += otherWds.name + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)
wds3 = Wds.Wds(info3)

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    wds2.refreshInfo()
    if wds1.isTurnOn and wds1.isChanged:
        sendMsg(wds1, [wds2, wds3])
    if wds2.isTurnOn and wds2.isChanged:
        sendMsg(wds2, [wds1, wds3])
    if wds3.isTurnOn and wds3.isChanged:
        sendMsg(wds3, [wds1, wds2])

