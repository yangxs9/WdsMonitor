import Wds
import time
import os

info1 = {
    'url': 'https://wds.modian.com/show_weidashang_pro/4786#1',
    'group': 'SNH48-张语格应援会',
    'qq': '132204035',
    'name': 'TAKO',
    'slogan': '丸子们的每一份心意对TAKO来说都非常重要，2017的夏天，一起为张语格的重返神七而加油吧！',
    'isTurnOn': True,
}

wds1 = Wds.Wds(info1)
print(wds1.getDays())