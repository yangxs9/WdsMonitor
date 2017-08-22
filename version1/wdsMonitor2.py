# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import time
import os

url = 'https://wds.modian.com/show_weidashang_pro/4135#1'
group = 'BEJ48-刘胜男应援会'
interval = 10

def getHtml(url):
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    try:
        with request.urlopen(req) as f:
            if f.status == 200:
                return f.read().decode('utf-8')
            else:
                print('error: cant get the page')
                return None
    except:
        print('error: cant get the page')
        return None

def getCommentsNum(html):
    if html == None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    commentNumTag = soup.select('.project-comment span')[0]
    return int(commentNumTag.string)

def getAddedUserInfo(html, addedNum):
    addedUserInfo= {}
    soup = BeautifulSoup(html, 'html.parser')
    userTags = soup.select('.list-comment .nick')
    infoTags = soup.select('.list-comment .nick_sup')
    for i in range(addedNum):
        user = userTags[i].string
        info = infoTags[i].string
        addedUserInfo[user] = info
    return addedUserInfo

def writeLog(logFile, log):
    try:  
        with open(logFile, 'a') as f:
            f.write(log)
    except:
        print('error: log failed')

def qqReport(addedUserInfo, group):
    localtime = time.asctime(time.localtime(time.time()))
    for user in addedUserInfo: 
        msg = user + ' 刚刚' + addedUserInfo[user] + '，感谢您对小树的支持！微打赏链接：http://t.cn/RSPzf7Y'    
        # log = localtime + ': ' + msg + '\n'
        # writeLog('log.txt', log)
        cmd = 'qq send group ' + group + ' ' + msg
        os.system(cmd)

def wdsMonitor(url, group, interval):
    html = getHtml(url)
    commentsNum = getCommentsNum(html)
    while True:
        time.sleep(interval)
        html = getHtml(url)
        if html == None:
            continue
        newcommentsNum = getCommentsNum(html)
        if newcommentsNum != None and newcommentsNum > commentsNum:
            addedNum = newcommentsNum - commentsNum
            commentsNum = newcommentsNum
            addedUserInfo = getAddedUserInfo(html, addedNum)
            qqReport(addedUserInfo, group)
            

wdsMonitor(url, group, interval)

