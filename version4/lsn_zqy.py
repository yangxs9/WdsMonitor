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

def sendMsg(mainWds, friendWds):
    msg = 'biu biu biu～'
    if mainWds.isChanged:
        for user in mainWds.addedUserMoney:
            msg += user + ' 刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！\n'
    msg += mainWds.activity + '正在进行中，目前情况：\n'
    msg += mainWds.name + '：' + str(mainWds.amount) + '元，' + str(mainWds.peopleNum) + '人参加\n'
    msg += friendWds.name + '：' + str(friendWds.amount) + '元，' + str(friendWds.peopleNum) + '人参加\n'
    
    msg += '本次活动结束将在今晚24点结束。\n'
    msg += mainWds.slogan
    msg += '微打赏链接：' + mainWds.url

    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)
lastTime = time.time()

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    currentTime = time.time()
    if wds1.isChanged or (currentTime - lastTime) > silence_interval:
        wds2.refreshInfo()          
        sendMsg(wds1, wds2)
        lastTime = currentTime

