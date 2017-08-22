# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 60

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4786#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'Tako',
    'slogan': '丸子们的每一份心意对Tako来说都非常重要，2017的夏天，一起为张语格的重返神七而加油吧！',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4786#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'Tako',
    'slogan': '丸子们的每一份心意对Tako来说都非常重要，2017的夏天，一起为张语格的重返神七而加油吧！',
    'isTurnOn': True,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def singleSend0(mainWds):
    if mainWds.isChanged == False:
        return False
    msg = 'Yummy，yummy！'
    for user in mainWds.addedUserMoney:
        msg += '感谢' + user + '在生诞集资中为布丁投下了' + str(mainWds.addedUserMoney[user]) + '个媛份！\n'
    msg += '目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '，一起为布丁加油鼓劲吧。\n'
    msg += '生日摩点平台：http://t.cn/RaQmiuF\n生诞支付宝：http://c.b0yp.com/h.UzNrMk?cv=oreDZtOz1L4&sm=17d897\n总选支付宝：http://c.b1yt.com/h.8Vanlr?cv=1TarZDISlbn&sm=804200\n总选限时jz活动：http://t.cn/RSuCU2N'
    # msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

def singleSend1(mainWds):
    if mainWds.isChanged == False:
        return False
    msg = 'Yummy，yummy！'
    for user in mainWds.addedUserMoney:
        msg += '感谢' + user + '在总选集资中为布丁投下了' + str(mainWds.addedUserMoney[user]) + '个媛份！\n'
    msg += '目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '，一起为布丁加油鼓劲吧。\n'
    msg += '生日摩点平台：http://t.cn/RaQmiuF\n生诞支付宝：http://c.b0yp.com/h.UzNrMk?cv=oreDZtOz1L4&sm=17d897\n总选支付宝：http://c.b1yt.com/h.8Vanlr?cv=1TarZDISlbn&sm=804200\n总选限时jz活动：http://t.cn/RSuCU2N'
    qqReport(msg, mainWds.qq)

def sendMsg(mainWds, others):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持！\n'
    msg += '甜品店对抗进行中，目前战况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    for otherWds in others:
        msg += otherWds.name + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)


wds0 = Wds.Wds(info0)
wds1 = Wds.Wds(info1)

while True:
    time.sleep(interval)
    wds0.refreshInfo()
    if wds0.isTurnOn and wds0.isChanged:
        singleSend0(wds0)
    wds1.refreshInfo()
    if wds1.isTurnOn and wds1.isChanged:
        singleSend1(wds1)

