# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import time
import os

url = 'https://wds.modian.com/ranking_list?pro_id=4135'
group = 'BEJ48-刘胜男应援会'
interval = 10

def getHtml(url):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    with request.urlopen(req) as f:
        if f.status == 200:
            return f.read().decode('utf-8')
        else:
            print('cant get the page')
            return None

def getWdsData(html):
    userMoney = {}
    soup = BeautifulSoup(html, 'html.parser')
    userTags = soup.select('#wrapper_jj .nickname')
    moneyTags = soup.select('#wrapper_jj .money')
    for i in range(len(userTags)):
        name = userTags[i].string
        moneyStr = moneyTags[i].string[1:]
        money = float(moneyStr)
        userMoney[name] = money
    return userMoney

def getUserMoney(url):
    html = getHtml(url)
    if html != None:
        userMoney = getWdsData(html)
        return userMoney
    else:
        return None

def getAddedUserMoney(userMoney, newUserMoney):
    addedUserMoney = {}
    for user in newUserMoney:
        if user not in userMoney:
            #print('new', user)
            addedUserMoney[user] = newUserMoney[user]
        elif userMoney[user] < newUserMoney[user]:
            addedUserMoney[user] = newUserMoney[user] - userMoney[user]
    return addedUserMoney

def qqReport(addedUserMoney, group):
    for user in addedUserMoney: 
        msg = user + ' 刚刚集资了 ' + str(addedUserMoney[user]) + '元，感谢您对小树的支持！微打赏链接：http://t.cn/RSPzf7Y'
        print(msg)
        cmd = 'qq send group ' + group + ' ' + msg
        os.system(cmd)

def wdsMonitor(url, group, interval):
    userMoney = getUserMoney(url)
    while True:
        time.sleep(interval)
        newUserMoney = getUserMoney(url)
        addedUserMoney = getAddedUserMoney(userMoney, newUserMoney)
        if len(addedUserMoney) == 0:
            print('no change')
        else:
            qqReport(addedUserMoney, group)
            userMoney = newUserMoney

wdsMonitor(url, group, interval)
