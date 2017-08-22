# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 180

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4887#1',
    'group': 'GNZ48-王盈应援会',
    'qq': '577236921',
    'name': '盈宝',
    'activity': 'GNZ48-王盈应援会四选中报集资活动',
    'slogan': '盈宝的生诞祭即将来临，那时候也将是四选中报的时候，在这个夏天，即使盈宝伤停公演，但是为了能让她在中报上听到她的名字，为了让她更有自信和底气，同时作为一份最好的生日礼物，大家一起来为她的光芒添砖加瓦吧！',
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

