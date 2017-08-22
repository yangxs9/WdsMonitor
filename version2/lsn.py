# -*- coding: utf-8 -*-

import Wds
import time
import os

lsn_url = 'https://wds.modian.com/show_weidashang_pro/4135#1'
group = 'BEJ48-刘胜男应援会'
interval = 300
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
            msg = msg + user + ' 刚刚支持了小树' + str(lsnWds.addedUserMoney[user]) + '元，'
        msg += '感谢大家的支持！微打赏链接：http://t.cn/RSPzf7Y'
    # writeLog(logFile, msg)
    qqReport(msg, group)
