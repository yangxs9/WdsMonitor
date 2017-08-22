# -*- coding: utf-8 -*-

import Wds
import time
import os

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

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def sendMsg(mainWds, friendWds, other1):
    lsnLast = 8274.90
    zqyLast = 6408.21
    xyyzLast = 19061.00
    lsnAmount = round(mainWds.amount - lsnLast, 2)
    zqyAmount = round(friendWds.amount - zqyLast, 2)
    xyyzAmount = round(other1.amount - xyyzLast, 2)

    msg = mainWds.activity + '今日战况：\n'
    sumAmount = round(lsnAmount + zqyAmount, 2)
    msg += mainWds.name + '+' + friendWds.name + '：' 
    msg += str(lsnAmount) + '+' + str(zqyAmount) + '=' + str(sumAmount) + '\n'    
    msg += other1.name + '：' + str(xyyzAmount) + '\n'

    if sumAmount > xyyzAmount:
        msg += '今天获胜的是【张琼予+刘胜男】'
    else:
        msg += '今天获胜的是【许杨玉琢】'
    
    # msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    # msg += mainWds.slogan
    # msg += '微打赏链接：' + mainWds.url
    print(msg)
    qqReport(msg, mainWds.qq)

countTime = 1500389999
now = time.time()
time.sleep(countTime - now)
wds1 = Wds.Wds(info1)
wds2 = Wds.Wds(info2)
wds3 = Wds.Wds(info3)
sendMsg(wds1, wds2, wds3)


