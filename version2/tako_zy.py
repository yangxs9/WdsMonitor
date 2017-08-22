# -*- coding: utf-8 -*-

import Wds
import time
import os

tako_url = 'https://wds.modian.com/show_weidashang_pro/4786#1'
zy_url = 'https://wds.modian.com/show_weidashang_pro/4785#1'
group = '132204035'
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

takoWds = Wds.Wds(tako_url)
zyWds = Wds.Wds(zy_url)

while True:
    time.sleep(interval)
    takoWds.refreshInfo()
    zyWds.refreshInfo()
    if takoWds.isChanged == False:
        continue
    msg = ''
    if takoWds.isChanged:
        for user in takoWds.addedUserMoney:
            msg = msg + user + ' 刚刚支持了Tako' + str(takoWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！'
    if zyWds.isChanged:
        msg = msg + '对方集资刚刚增长了' + str(zyWds.addedAmount) + '元。'
    msg += '目前比分Tako'
    msg = msg + str(takoWds.amount) + ':' + str(zyWds.amount) + '赵粤，'
    if takoWds.amount < zyWds.amount:
        msg += 'Tako暂时落后，'
    elif takoWds.amount > zyWds.amount:
        msg += 'Tako暂时领先，'
    else:
        msg += '暂时打平。'
    msg += '丸子们的每一份心意对TAKO来说都非常重要，2017的夏天，一起为张语格的重返神七而加油吧！微打赏链接：' + tako_url
    # writeLog(logFile, msg)
    qqReport(msg, group)
