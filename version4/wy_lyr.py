# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 100

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5139#1',
    'group': 'GNZ48-王盈应援会',
    'qq': '577236921',
    'name': '盈宝',
    'activity': '贼队厨神争霸赛',
    'slogan': '',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5120#1',
    'group': '',
    'qq': '',
    'name': '龙亦瑞',
    'activity': '',
    'slogan': '',
    'isTurnOn': False,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)

def sendMsg(mainWds, otherWds):
    msg = ''
    if mainWds.isChanged:
        for user in mainWds.addedUserMoney:
            msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！\n'
    if otherWds.isChanged:
        msg += '对方刚刚增长了' + str(otherWds.addedAmount) + '元。\n'
    msg += mainWds.activity + '正在进行中，目前情况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    msg += otherWds.name + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    wds2.refreshInfo()
    if wds1.isChanged or wds2.isChanged:
        sendMsg(wds1, wds2)
