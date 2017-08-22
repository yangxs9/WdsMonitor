# -*- coding: utf-8 -*-

import Wds
import time
import os
import socket

socket.setdefaulttimeout(50)
interval = 180
silence_interval = 10000.0

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4135#1',
    'group': 'BEJ48-刘胜男应援会',
    'qq': '548718867',
    'name': '小树',
    'activity': '刘胜男应援会四选众筹计划',
    'slogan': '园丁们的每一份力量对小树都很重要，这个夏天一起为小树加油吧！',
    'isTurnOn': True,
}

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
        msg += '感谢大家对支持！\n'
    msg += mainWds.activity + '正在进行中，目标金额35000元，目前总额' + str(mainWds.amount) + '元，' + '参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
lastTime = time.time()

while True:
    time.sleep(interval)
    try:
        wds1.refreshInfo()
    except:
        print('refresh error')
    currentTime = time.time()
    if wds1.isChanged or (currentTime - lastTime) > silence_interval:
        singleSend(wds1)
        lastTime = currentTime

