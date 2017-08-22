# -*- coding: utf-8 -*-

import Wds
import time
import os

interval = 80

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/5587#1',
    'rankUrl': 'https://wds.modian.com/ranking_list?pro_id=5587',
    'group': 'SHY48-王诗蒙应援会',
    'qq': '21070782',
    'name': '王诗蒙',
    'activity': '王诗蒙拉票专项',
    'goal': 10000,
    'slogan': '',
    'isTurnOn': True,
}

def qqReport(msg, group):
    msg = "'" + msg + "'"
    cmd = 'qq send group ' + group + ' ' + msg
    os.system(cmd)
    # print(msg)

def ranking(user, rank):
    order = None
    for i in range(len(rank)):
        if user in rank[i]:
            order = i
    if order == None:
        return '当前排名20名以后，请继续加油！'
    return '当前排名第' + order + '，请继续加油！'

def singleSend(mainWds):
    if mainWds.isChanged == False:
        return False
    msg = ''
    for user in mainWds.addedUserMoney:
        msg += user + '刚刚支持了' + mainWds.name + str(mainWds.addedUserMoney[user]) + '元，'
        msg += ranking(user, mainWds.rank)
    msg += '感谢大家对支持！\n'
    msg += mainWds.activity + '正在进行中，目前总额' + str(mainWds.amount) + '元，' + '目标金额' + str(mainWds.goal) + '，参加人数' + str(mainWds.peopleNum) + '，'
    msg += '距离本次活动结束还有' + str(mainWds.time) + '。\n'
    msg += mainWds.slogan + '微打赏链接：' + mainWds.url
    qqReport(msg, mainWds.qq)

wds1 = Wds.Wds(info1)
wds1.getRank();

while True:
    time.sleep(interval)
    wds1.refreshInfo()
    if wds1.isTurnOn and wds1.isChanged:
        singleSend(wds1)
