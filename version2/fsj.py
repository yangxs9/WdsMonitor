# -*- coding: utf-8 -*-

import Wds
import time
import os

lsn_url = 'https://wds.modian.com/show_weidashang_pro/3950'
group = 'BEJ48-冯思佳应援会'
interval = 180
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

lsnWds = Wds.Wds(lsn_url)

while True:
    time.sleep(interval)
    lsnWds.refreshInfo()
    if lsnWds.isChanged == False:
        continue
    msg = ''
    if lsnWds.isChanged:
        for user in lsnWds.addedUserMoney:
            msg = msg + user + ' 刚刚支持了小北' + str(lsnWds.addedUserMoney[user]) + '元，'
        msg += '总选众筹正在火热进行中，请大家为我们的小北奉上我们的力量吧，微打赏链接：https://wds.modian.com/show_weidashang_pro/3950'
    # writeLog(logFile, msg)
    qqReport(msg, group)
