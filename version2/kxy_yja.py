# -*- coding: utf-8 -*-

import Wds
import time
import os

main_url = 'https://wds.modian.com/show_weidashang_pro/4813#1'
other_url = 'https://wds.modian.com/show_weidashang_pro/4814#1'
group = 'SNH48-孔肖吟应援会'
mainName = '小孔'
otherName = '嘉爱'
interval = 60
logFile = 'log.txt'

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)

def writeLog(logFile, msg):
    try:  
        with open(logFile, 'a') as f:
            localtime = time.asctime(time.localtime(time.time()))
            log = localtime + ': ' + msg + '\n'
            f.write(log)
    except:
        print('error: log failed')

mainWds = Wds.Wds(main_url)
otherWds = Wds.Wds(other_url)

while True:
    time.sleep(interval)
    mainWds.refreshInfo()
    otherWds.refreshInfo()
    if mainWds.isChanged == False:
        continue
    msg = ''
    if mainWds.isChanged:
        for user in mainWds.addedUserMoney:
            msg += user + ' 刚刚支持了' + mainName + str(mainWds.addedUserMoney[user]) + '元，'
        msg += '总共增长了' + str(mainWds.addedAmount) + '元，'
        msg += '感谢大家的支持！\n'
    if otherWds.isChanged:
        msg += '对方集资刚刚增长了' + str(otherWds.addedAmount) + '元。\n'
    msg += '目前战况：\n'
    msg += mainName + '：' + str(mainWds.amount) + '，' + '参加人数' + str(mainWds.peopleNum) + '\n'
    msg += otherName + '：' + str(otherWds.amount) + '，' + '参加人数' + str(otherWds.peopleNum) + '\n'
    if mainWds.amount < otherWds.amount:
        msg += '我们暂时落后' + str(round(otherWds.amount - mainWds.amount, 2)) + '元。\n'
    elif mainWds.amount > otherWds.amount:
        msg += '我们暂时领先' + str(round(mainWds.amount - otherWds.amount, 2)) + '元。\n'
    else:
        msg += '我们暂时打平。\n'
    msg += '音符们的每一份心意对于小孔来说都是非常重要的，今年这个夏天，让我们不留遗憾，冲击选拔！！微打赏链接：' + main_url
    # writeLog(logFile, msg)
    qqReport(msg, group)
