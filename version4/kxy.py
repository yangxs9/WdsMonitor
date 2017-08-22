# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 80

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5603#1',
    'group': 'SNH48-孔肖吟应援会',
    'qq': '221771881',
    'name': '小孔',
    'activity': 'SNH48-孔肖吟应援会中报冲刺——剑指选拔',
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
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + '刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家对支持！\n'
    msg += mainWds.activity + '正在进行中，目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    if wds1.isTurnOn and wds1.isChanged:
        singleSend(wds1)

