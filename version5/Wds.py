from urllib import request
from bs4 import BeautifulSoup

class Wds(object):

    def __init__(self, info):
        super(Wds, self).__init__()
        self.url = info['url']
        self.rankUrl = info['rankUrl']
        self.group = info['group']
        self.qq= info['qq']
        self.name = info['name']
        self.activity = info['activity']
        self.goal = info['goal']
        self.slogan = info['slogan']
        self.isTurnOn = info['isTurnOn']
        
        self.html = self.getHtml()
        self.amount = self.getAmount()
        self.peopleNum = self.getPeopleNum()
        self.time = self.getTime()
        self.isChanged = False
        self.addedAmount = 0
        self.addedUserMoney = {}
        self.rank = []

    def getHtml(self):
        req = request.Request(self.url)
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

    def getCommentsNum(self):
        if self.html == None:
            return None
        soup = BeautifulSoup(self.html, 'html.parser')
        commentNumTag = soup.select('.project-comment span')[0]
        return int(commentNumTag.string)

    def getAmount(self):
        if self.html == None:
            return None
        soup = BeautifulSoup(self.html, 'html.parser')
        amountTag = soup.select('.current span')[1]
        amountStr = amountTag.next_element.next_element.next_element
        return round(float(amountStr.replace(',', '')), 2)

    def getAddedUserMoney(self):
        if self.html == None or self.addedAmount == 0:
            return {}
        addedUserMoney = {}
        soup = BeautifulSoup(self.html, 'html.parser')
        userTags = soup.select('.list-comment .nick')
        infoTags = soup.select('.list-comment .nick_sup')
        try:
            i = 0
            amount = 0.0
            while round(amount, 2) < round(self.addedAmount, 2) and i < len(userTags):
                user = userTags[i].string
                info = infoTags[i].string
                money = round(float(info[3:-1]), 2)
                addedUserMoney[user] = money
                amount += money
                i += 1
        except:
            print('error: cant get addedUserMoney ')
            return {}
        return addedUserMoney

    def getPeopleNum(self):
        if self.html == None:
            return None
        soup = BeautifulSoup(self.html, 'html.parser')
        peopleNum = soup.select('.b span')[0].string
        return int(peopleNum)

    def getTime(self):
        if self.html == None:
            return None
        soup = BeautifulSoup(self.html, 'html.parser')
        num = soup.select('.right em')[0].string
        unit = soup.select('.right span')[0].next_element.next_element.next_element.next_element
        unit = unit.strip()
        return num + unit

    def getRank(self):
        req = request.Request(self.rankUrl)
        req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
        try:
            with request.urlopen(req) as f:
                if f.status == 200:
                    rankHtml = f.read().decode('utf-8')
                else:
                    print('error: cant get the rank page')
                    return None
        except:
            print('error: cant get the rank page')
            return None
        rank = []
        soup = BeautifulSoup(rankHtml, 'html.parser')
        userTags = soup.select('.people_list .nickname')
        moneyTags = soup.select('.people_list .money')
        for i in range(len(userTags)):
            if i < 20:
                moneyStr = moneyTags[i].string[1:].replace(',','')
                money = round(float(moneyStr), 2)
                rank.append({userTags[i].string: money})
        return

    def refreshInfo(self):
        self.html = self.getHtml()
        newAmount = self.getAmount()
        if newAmount != None and newAmount > self.amount:
            self.addedAmount = round(newAmount - self.amount, 2)
            self.addedUserMoney = self.getAddedUserMoney()
            self.amount = newAmount
            self.peopleNum = self.getPeopleNum()
            self.rank = self.getRank()
            self.time = self.getTime()
            self.isChanged = True 
        else:
            self.isChanged = False
            self.addedAmount = 0
            self.addedUserMoney = {}
