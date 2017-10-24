import json
from WdsMonitor import BasicClient, WdsClient, Receiver, Monitor

def loadConfig(file='./config.json'):
    with open('config.json', 'r') as file:
        config = json.load(file)
    
    receivers = []
    for receiver in config['receivers']:
        main = receiver['main']
        mainClient = WdsClient(main['id'], main['postId'], main['name'])
        # html = mainClient.getCommentHtml()
        # print(mainClient.getAddedUserMoney(html,1400))
        otherClients = []
        for other in receiver['others']:
            otherClients.append(BasicClient(other['id'], other['name']))
        receivers.append(Receiver(receiver['qq'], mainClient, otherClients, receiver['info'], receiver['options']))

    monitor = Monitor(receivers)
    monitor.run(config['interval'])

loadConfig()