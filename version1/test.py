# -*- coding: utf-8 -*-

import Wds2
import time
import os

lsn_url = 'https://wds.modian.com/show_weidashang_pro/4559#1'
lsnWds = Wds2.Wds(lsn_url)

print(lsnWds.getAddedUserMoney(330.0))