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
    'url': 'https://wds.modian.com/show_weidashang_pro/4785#1',
    'group': '赵粤老婆团',
    'qq': '',
    'name': '赵粤',
    'slogan': '',
    'isTurnOn': False,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    # os.system(cmd)
    print(msg)

def sendMsg(mainWds, otherWds):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
    # msg += '总共增长了' + str(mainWds.addedAmount) + '元，'
    msg += '感谢大家的支持！\n'
    if otherWds.isChanged:
        msg += '对方集资刚刚增长了' + str(otherWds.addedAmount) + '元。\n'
    msg += '目前战况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    msg += otherWds.name + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    if mainWds.amount < otherWds.amount:
        msg += '我们暂时落后' + str(round(otherWds.amount - mainWds.amount, 2)) + '元，'
    elif mainWds.amount > otherWds.amount:
        msg += '我们暂时领先' + str(round(mainWds.amount - otherWds.amount, 2)) + '元，'
    else:
        msg += '我们暂时打平，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    wds2.refreshInfo()
    if wds1.isTurnOn and wds1.isChanged:
        sendMsg(wds1, wds2)
    if wds2.isTurnOn and wds2.isChanged:
        sendMsg(wds2, wds1)
