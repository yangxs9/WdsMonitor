#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
import time
import sys
import os
from cqsdk import CQBot, CQAt, CQImage, RcvdPrivateMessage, RcvdGroupMessage, SendGroupMessage, GetGroupMemberList, RcvGroupMemberList


class Monitor(object):

    def __init__(self, receivers, isCoolQ):
        self.receivers = receivers
        self.isCoolQ = isCoolQ
        if self.isCoolQ:
            self.qqbot = CQBot(11235)
            self.qqbot.start()
            # self.qqbot.send(SendGroupMessage("21070782", "test"))
            print("QQBot is running...")

    def run(self, interval):
        print('start')
        while True:
            time.sleep(interval)
            for receiver in self.receivers:
                messages = receiver.getMessages()
                if messages != None:
                    for msg in messages:
                        self.send(receiver.qq, msg)

    def send(self, qq, message):
        print(message)
        if self.isCoolQ:
            self.qqbot.send(SendGroupMessage(qq, message))
        else:
            message = "'" + message + "'"
            cmd = 'qq send group ' + qq + ' ' + message
            # cmd = 'qq send buddy 407190960 ' + message
            os.system(cmd)


class Receiver(object):

    def __init__(self, qq, mainClient, otherClients, info, options):
        self.qq = qq
        self.mainClient = mainClient
        self.otherClients = otherClients
        self.info = info
        self.options = options

    def getMessages(self, messager=None):
        isRank = self.options['total'] or self.options['rank'] or self.options['top']
        if self.mainClient.updated(isRank):
            for client in self.otherClients:
                client.updated()
            if messager == None:
                messager = self.defaultMessager
            return messager(self.mainClient, self.otherClients, self.info, self.options)
        return None

    def defaultMessager(self, mainClient, otherClients, info, options):
        messages = []
        message = info['start']
        for user, money in mainClient.addedUserMoney.items():
            message += user + '刚刚支持了' + str(money) + '元，'
            if options['total']:
                total = mainClient.getTotal(user)
                if total != None:
                    message += '累积支持' + str(total) + '元，'
            if options['rank']:
                rank = mainClient.getUserRank(user)
                if rank != None:
                    message += '当前排名第' + str(rank) + '。'
        message += '感谢大家对' + mainClient.name + '每一份的支持！\n'
        
        message += info['project'] + '正在进行中，'
        message += '目前金额' + str(mainClient.amount) + '元，'
        if mainClient.amount < info['goal']:
            message += '离目标' + str(info['goal']) + '还差' + str(round(info['goal'] - mainClient.amount,2)) + '元，'
        message += '参加人数' + str(mainClient.peopleNum) + '，'   
        leftTime = self.leftTime(info['due'])
        if leftTime:
            message += '距离本次活动结束还剩' + leftTime + '。\n'
        else:
            message += '本次活动已结束，感谢大家的参与！'
        
        if options['top'] and mainClient.rank != None and len(mainClient.rank) > 0:
            message += '聚聚榜Top10：'
            length = min(10, len(mainClient.rank))
            for i in range(length):
                message += str(i + 1) + '.' + mainClient.rank[i][1] + ': ' + str(mainClient.rank[i][0]) + ', '
            message += '\n'

        if len(otherClients) > 0:
            message += '目前PK情况：'
            for client in otherClients:
                message += client.name +': ' + str(client.amount) + '元,'
            message += '\n'

        message += info['end']
        messages.append(message)
        messages.append(info['link'])
        return messages

    def leftTime(self, due):
        now = time.time()
        leftSeconds = due - now
        if leftSeconds < 0:
            return False
        days = int(leftSeconds / (3600 * 24))
        leftSeconds = leftSeconds % (3600 * 24)
        hours = int(leftSeconds / 3600)
        leftSeconds = leftSeconds % 3600
        minutes = int(leftSeconds / 60)
        if days != 0:
            return str(days) + '天' + str(hours) + '小时' + str(minutes) + '分钟'
        elif hours != 0:
            return str(hours) + '小时' + str(minutes) + '分钟'
        else:
            return str(minutes) + '分钟'


class BasicClient(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        html = self.getHtml()
        self.amount = self.getAmount(html)
        self.peopleNum = self.getPeopleNum(html)
        self.time = self.getTime(html)
        self.addedAmount = 0
        print('client initialization done:', self.name, self.amount, self.peopleNum, self.time)

    def updated(self):
        html = self.getHtml()
        if html == None:
            return False
        newAmount = self.getAmount(html)
        if self.amount == None:
            amount = newAmount
        if newAmount != None and newAmount > self.amount:
            self.addedAmount = round(newAmount - self.amount, 2)
            self.amount = newAmount
            self.peopleNum = self.getPeopleNum(html)
            self.time = self.getTime(html)
            return True
        return False


    def getHtml(self):
        url = 'https://wds.modian.com/show_weidashang_pro/' + self.id
        try:
            headers={'Accepat':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            return response.text
        except:
            print("Error: can't get html.")
            return None

    def getAmount(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            amountTag = soup.select('.current span')[1]
            amountStr = amountTag.next_element.next_element.next_element
            return round(float(amountStr.replace(',', '')), 2)
        except:
            print("Error: can't get amount.")
            return None        

    def getPeopleNum(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            peopleNum = soup.select('.b span')[0].string
            return int(peopleNum)
        except:
            print('Error: cant get peopleNum.')
            return None

    def getTime(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            num = soup.select('.right em')[0].string
            unit = soup.select('.right em')[0].next_element.next_element
            unit = unit.strip()
            return num + unit
        except:
            print('Error: cant get time.')
            return None


class WdsClient(BasicClient):

    def __init__(self, id, postId, name):
        BasicClient.__init__(self, id, name)
        self.postId = postId
        self.addedUserMoney = {}
        self.userMoney = {}
        self.rank = []

    def updated(self, isRank):
        html = self.getHtml()
        commentHtml = self.getCommentHtml()
        if html == None or commentHtml == None:
            return False
        newAmount = self.getAmount(html)
        print(self.name, newAmount)
        if newAmount != None and newAmount > self.amount:
            self.addedAmount = round(newAmount - self.amount, 2)
            self.addedUserMoney = self.getAddedUserMoney(commentHtml, self.addedAmount)
            if self.addedUserMoney != None and len(self.addedUserMoney) > 0:
                self.amount = newAmount
                self.peopleNum = self.getPeopleNum(html)
                self.time = self.getTime(html)
                if isRank:
                    self.userMoney = self.getUserMoney()
                    self.rank = self.getRank(self.userMoney)
                return True
        return False

    def getCommentHtml(self):
        url = 'https://wds.modian.com/ajax/comment_list'
        params = {
            'page': 1,
            'post_id': self.postId,
            'pro_id': self.id
        }
        try:
            headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            response = requests.post(url, data=params, headers=headers, timeout=10)
            return response.json()['data']['html']
        except:
            print("Error: can't get comment html.")
            return None

    def getAddedUserMoney(self, html, addedAmount):
        if addedAmount == 0:
            return {}  
        try:
            addedUserMoney = {}
            soup = BeautifulSoup(html, 'html.parser')
            userTags = soup.select('.nick')
            infoTags = soup.select('.nick_sup')
            i = 0
            amount = 0.0
            while round(amount, 2) < round(addedAmount, 2) and i < len(userTags):
                user = userTags[i].string
                info = infoTags[i].string
                money = round(float(info[3:-1]), 2)
                if user in addedUserMoney:
                    addedUserMoney[user] += money
                else:
                    addedUserMoney[user] = money
                amount += money
                i += 1
            return addedUserMoney
        except:
            print('Error: cant get addedUserMoney.')
            return None
        
    def getRankHtml(self):
        url = 'https://wds.modian.com/ajax/backer_ranking_list'
        params = {
            'pro_id': self.id,
            'type':1,
            'page':1,
            'page_size':50,
        }
        try:
            headers={'Accepat':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            response = requests.post(url, data=params, headers=headers, timeout=10)
            return response.json()['data']['html']
        except:
            print("Error: can't get rank html.")
            return None

    def getUserMoney(self):
        html = self.getRankHtml()
        if html == None:
            return None
        try:
            soup = BeautifulSoup(html, 'html.parser')
            userTags = soup.select('.nickname')
            moneyTags = soup.select('.money')
            userMoney = {}
            for i in range(len(userTags)):
                user = userTags[i].string
                moneyStr = moneyTags[i].string
                userMoney[user] = self.moneyNum(moneyStr)
            return userMoney
        except:
            print("Error: can't get userMoney.")
            return None

    def getTotal(self, user):
        if self.userMoney == None:
            return None
        if user in self.userMoney:
            return self.userMoney[user]
        return None

    def getRank(self, userMoney):
        if userMoney == None:
            return None
        try:
            rank = [(money, user) for user, money in userMoney.items()]
            rank.sort()
            rank.reverse()
            return rank
        except:
            print("Error: can't get rank.")
            return None
   
    def getUserRank(self, user):
        if self.rank == None:
            return None
        for i in range(len(self.rank)):
            if self.rank[i][1] == user:
                return i + 1
        return None

    def moneyNum(self, moneyStr):
        try:
            moneyStr = moneyStr.replace(',', '')
            moneyStr = moneyStr.replace('¥', '')
            moneyStr = moneyStr.strip()
            return round(float(moneyStr), 2)
        except:
            print("Error: can't convert moneyStr.")
            return None


def run(file='./config.json'):
    with open(file, 'r', encoding="utf-8") as file:
        config = json.load(file)
    
    receivers = []
    for receiver in config['receivers']:
        main = receiver['main']
        mainClient = WdsClient(main['id'], main['postId'], main['name'])
        otherClients = []
        for other in receiver['others']:
            otherClients.append(BasicClient(other['id'], other['name']))
        receivers.append(Receiver(receiver['qq'], mainClient, otherClients, receiver['info'], receiver['options']))

    monitor = Monitor(receivers, config['isCoolQ'])
    monitor.run(config['interval'])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run()
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("Usage: python3 WdsMonitor.py file")
    



