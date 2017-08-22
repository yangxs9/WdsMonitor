# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180
silence_interval = 10000.0

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5858#1',
    'group': 'BEJ48-刘胜男应援会',
    'qq': '548718867',
    'name': '小树',
    'activity': '前辈等等我争夺战',
    'slogan': '园丁们的每一份力量对小树都很重要，这个夏天一起为小树加油吧！',
    'isTurnOn': True,
}

info2 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5859#1',
    'group': '',
    'qq': '',
    'name': 'soso',
    'activity': '前辈等等我争夺战',
    'slogan': '',
    'isTurnOn': False,
}

info3 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5862#1',
    'group': '',
    'qq': '',
    'name': '绵羊',
    'activity': '前辈等等我争夺战',
    'slogan': '',
    'isTurnOn': False,
}

def isTime():
    currentTime = time.gmtime(time.time())

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def singleSend(mainWds):
    msg = 'biu biu biu～'
    if mainWds.isChanged:
        for user in mainWds.addedUserMoney:
            msg += user + '刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！\n'
    msg += mainWds.activity + '正在进行中，目标金额35000元，目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

def sendMsg(mainWds, friendWds, other1):
    lsnAmount = round(mainWds.amount - 8274.90, 2)
    zqyAmount = round(friendWds.amount - 6408.21, 2)
    xyyzAmount = round(other1.amount - 19061.00, 2)
    msg = 'biu biu biu～'
    if mainWds.isChanged:
        for user in mainWds.addedUserMoney:
            msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！\n'
    if other1.isChanged:
        msg += '刚刚对方增长了' + str(other1.addedAmount) + '元。\n'
    msg += mainWds.activity + '正在进行中，今日情况：\n'
    sumAmount = round(lsnAmount + zqyAmount, 2)
    msg += mainWds.name + '+' + friendWds.name + '：' 
    msg += str(lsnAmount) + '+' + str(zqyAmount) + '=' + str(sumAmount) + '\n'    
    msg += other1.name + '：' + str(xyyzAmount) + '\n'

    if sumAmount > xyyzAmount:
        msg += '我们暂时领先' + str(round(sumAmount - xyyzAmount, 2)) + '元。\n'
    else:
        msg += '我们暂时落后' + str(round(xyyzAmount - sumAmount, 2)) + '元。\n'
    
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan
    msg += '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)
wds3 = Wds.Wds(info3)
lastTime = time.time()

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    currentTime = time.time()
    if wds1.isChanged or (currentTime - lastTime) > silence_interval:
        wds2.refreshInfo()
        wds3.refreshInfo()            
        sendMsg(wds1, wds2, wds3)
        lastTime = currentTime

