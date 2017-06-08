from urllib import request
from bs4 import BeautifulSoup

class Wds(object):

    def __init__(self, url):
        super(Wds, self).__init__()
        self.url = url
        self.html = self.getHtml(url)
        self.amount = self.getAmount(self.html)
        self.commentsNum = self.getCommentsNum(self.html)
        self.isChanged = False
        self.addedAmount = 0
        self.addedNum = 0
        self.addedUserInfo = {}

    def getHtml(self, url):
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

    def getCommentsNum(self, html):
        if html == None:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        commentNumTag = soup.select('.project-comment span')[0]
        return int(commentNumTag.string)

    def getAmount(self, html):
        if html == None:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        amountTag = soup.select('.current span')[1]
        amountStr = amountTag.next_element.next_element.next_element
        return float(amountStr.replace(',', ''))

    def getAddedUserInfo(self, html, addedNum):
        addedUserInfo= {}
        soup = BeautifulSoup(html, 'html.parser')
        userTags = soup.select('.list-comment .nick')
        infoTags = soup.select('.list-comment .nick_sup')
        for i in range(addedNum):
            user = userTags[i].string
            info = infoTags[i].string
            addedUserInfo[user] = info
        return addedUserInfo

    def refreshInfo(self):
        self.html = self.getHtml(self.url)
        newAmount = self.getAmount(self.html)
        if newAmount > self.amount:
            self.isChanged = True
            self.addedAmount = newAmount - self.amount
            self.amount = newAmount
            newCommentsNum = self.getCommentsNum(self.html)
            self.addedNum = newCommentsNum - self.commentsNum
            self.addedUserInfo = self.getAddedUserInfo(self.html, self.addedNum)
            self.commentsNum = newCommentsNum
        else:
            self.isChanged = False
