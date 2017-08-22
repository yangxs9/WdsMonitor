# -*- coding: utf-8 -*-

import Wds
import time
import os

url = 'https://wds.modian.com/show_weidashang_pro/3708#1'
group = '132204035'
interval = 60

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

wds = Wds.Wds(url)

while True:
    time.sleep(interval)
    wds.refreshInfo()
    if wds.isChanged == False:
        continue
    msg = ''
    for user in wds.addedUserMoney:
        msg = msg + user + ' 刚刚支持了TAKO' + str(wds.addedUserMoney[user]) + '元，'
    msg += '感谢大家的支持，丸子们的每一份心意对TAKO来说都非常重要，2017的夏天，一起为张语格的重返神七而加油吧！微打赏链接：' + url
    # writeLog(logFile, msg)
    qqReport(msg, group)
