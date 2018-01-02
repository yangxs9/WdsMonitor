#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
from WdsMonitor import BasicClient, WdsClient, Receiver, Monitor 

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
        print("Usage: python3 monitor.py file")