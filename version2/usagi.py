# -*- coding: utf-8 -*-

import Wds
import time
import os

url = 'https://wds.modian.com/show_weidashang_pro/4220#1'
group = 'GNZ48-冼燊楠应援会'
interval = 600

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
        msg = msg + user + ' 刚刚支持了' + str(wds.addedUserMoney[user]) + '元，'
    msg += '感谢您的支持～夏天已经来临，一起为兔子的梦想添砖加瓦吧！微打赏链接：' + url
    # writeLog(logFile, msg)
    qqReport(msg, group)
