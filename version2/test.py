# -*- coding: utf-8 -*-

import Wds
import time
import os

lsn_url = 'https://wds.modian.com/show_weidashang_pro/4135#1'

lsnWds = Wds.Wds(lsn_url)

lsnWds.getDays()