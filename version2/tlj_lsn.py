# -*- coding: utf-8 -*-

import Wds
import time
import os

lsn_url = 'https://wds.modian.com/show_weidashang_pro/4559#1'
tlj_url = 'https://wds.modian.com/show_weidashang_pro/4558#1'
group = '454388286'
interval = 180

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

lsnWds = Wds.Wds(lsn_url)
tljWds = Wds.Wds(tlj_url)

while True:
    time.sleep(interval)
    lsnWds.refreshInfo()
    tljWds.refreshInfo()
    if lsnWds.isChanged == False and tljWds.isChanged == False:
        continue
    msg = ''
    if tljWds.isChanged:
        for user in tljWds.addedUserMoney:
            msg = msg + user + ' 刚刚支持了Liga' + str(tljWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！'
    if lsnWds.isChanged:
        msg = msg + '小树集资刚刚增长了' + str(lsnWds.addedAmount) + '元。'
    msg += '【北广暗黑拯救战】唐莉佳x刘胜男联合企划正在进行中，目前比分Liga'
    msg = msg + str(tljWds.amount) + ':' + str(lsnWds.amount) + '小树，'
    if lsnWds.amount < tljWds.amount:
        msg += 'Liga暂时领先，'
    elif lsnWds.amount > tljWds.amount:
        msg += 'Liga暂时落后，'
    else:
        msg += '暂时打平。'
    msg += '为了让Liga远离豆汁的威胁，大家加油集资吧！微打赏链接：' + tlj_url
    # writeLog(logFile, msg)
    qqReport(msg, group)
