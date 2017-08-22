# -*- coding: utf-8 -*-

import Wds
import time
import os

main_url = 'https://wds.modian.com/show_weidashang_pro/4686#1'
other1_url = 'https://wds.modian.com/show_weidashang_pro/4684#1'
other2_url = 'https://wds.modian.com/show_weidashang_pro/4687#1'
other3_url = 'https://wds.modian.com/show_weidashang_pro/4685#1'

#group = 'BEJ48-冯思佳应援会'
group = '空'
interval = 60
logFile = 'log.txt'

def qqReport(msg, group):
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

def order(mainAmout, amount1, amount2, amount3):
    oder = 4
    if mainAmout >= amount1:
        order --
    if mainAmout >= amount1:
        order --
    if mainAmout >= amount1:
        order --
    return str(order)



mainWds = Wds.Wds(main_url)
other1Wds = Wds.Wds(other1_url)
other2Wds = Wds.Wds(other2_url)
other3Wds = Wds.Wds(other3_url)

while True:
    time.sleep(interval)
    mainWds.refreshInfo()
    if mainWds.isChanged == False or mainWds.addedUserInfo == None:
        continue
    other1Wds.refreshInfo()
    other2Wds.refreshInfo()
    other3Wds.refreshInfo()
    msg = ''
    for user in mainWds.addedUserInfo:
        msg = msg + user + ' 刚刚支持了小北' + mainWds.addedUserInfo[user][3:] + '，'
    msg = msg + '，【女神之战】正在火热进行中，目前小北的金额是' + str(mainWds.amount)
    msg = msg + '其他三家的金额是' + str(other1Wds.amount) + '，' + str(other2Wds.amount) + '，' + str(other3Wds.amount) + '。' 
    msg = msg + '我们现在是第' + order(mainWds.amout, other1Wds.amount, other2Wds.amount, other3Wds.amount) + '名，'
    msg += '请大家为我们的黑夜女神小北奉上我们的力量吧，微打赏链接：https://wds.modian.com/show_weidashang_pro/4686#1'
    # writeLog(logFile, msg)
    qqReport(msg, group)
