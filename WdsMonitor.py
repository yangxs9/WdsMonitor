import requests
from bs4 import BeautifulSoup
import time
import os


class Monitor(object):

    def __init__(self, receivers):
        self.receivers = receivers

    def run(self, interval):
        print('start')
        while True:
            time.sleep(interval)
            for receiver in self.receivers:
                receiver.check()


class Receiver(object):

    def __init__(self, qq, mainClient, otherClients, info, options):
        self.qq = qq
        self.mainClient = mainClient
        self.otherClients = otherClients
        self.info = info
        self.options = options

    def check(self):
        # print('checking for', self.qq)
        isRank = self.options['total'] or self.options['rank'] or self.options['top']
        if self.mainClient.updated(isRank):
            for client in self.otherClients:
                client.updated()
            self.send()

    def send(self, messager=None):
        if messager == None:
            messager = self.defaultMessager
        message = messager(self.mainClient, self.otherClients, self.info, self.options)
        if message != None:
            print(message)
        message = "'" + message + "'"
        cmd = 'qq send group ' + self.qq + ' ' + message
        os.system(cmd)

    def defaultMessager(self, mainClient, otherClients, info, options):
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
        message += '距离本次活动结束还有' + str(mainClient.time) + '。\n'
        
        if options['top'] and mainClient.rank != None and len(mainClient.rank) > 0:
            message += '聚聚榜Top10：'
            length = min(10, len(mainClient.rank))
            for i in range(length):
                message += str(i + 1) + '.' + mainClient.rank[i][1] + ': ' + str(mainClient.rank[i][0]) + ','
            message += '\n'

        if len(otherClients) > 0:
            message += '目前PK情况：'
            for client in otherClients:
                message += client.name +': ' + str(client.amount) + '元,'
            message += '\n'

        message += info['end']
        return message


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
            response = requests.get(url)
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
            response = requests.post(url, data=params)
            return response.json()['data']['html']
        except:
            print("Error: can't get rank html.")
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
            response = requests.post(url, data=params)
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




