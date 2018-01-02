# WdsMonitor 微打赏监控机器人

WdsMonitor is an application that checks updates for projects on [微打赏](https://wds.modian.com/) and send message to QQ group when there is any update.

微打赏监控机器人可以定时检查指定微打赏项目的更新并发送提醒消息到QQ群

## Features
* 更改配置即可使用
* 一个程序可同时监控多个项目发送多个qq群
* 可自定义消息内容函数
* 支持qqbot和酷Q
* 运行稳定，有容错机制


## Dependencies
* Python3
* requests
* bs4
* [qqbot](https://github.com/pandolia/qqbot) or [CoolQ](https://cqp.cc/)

酷Q环境的搭建参考：https://github.com/jqqqqqqqqqq/coolq-telegram-bot

## Usage

先运行qqbot或酷q

```
python monitor.py config.json
```

使用json文件传入参数，示例说明：

```json
{
    "interval": 60, //每次更新间隔时间
    "isCoolQ": false, //是否使用酷q，否则使用qqbot
    "receivers": [ //接收信息
        {
            "qq": "548718867", //群号
            "main": { //监控项目
                "id": "8565", //项目id
                "postId": "17940", //可在项目页面comment_list的请求中找到
                "name": "小树" 
            },
            "others": [ //PK对象
                {"id": "8179", "name": "布丁"}
            ],
            "info": {
                "project": "金曲大赏三日限定集资", 
                "goal": 30000, //目标金额
                "due": 1509109020, //截止时间，UTC时间的timestamp
                "start": "biu biu biu～",
                "end": "一起加油让小树站上她所热爱的大舞台吧！",
                "link": "微打赏链接：https://wds.modian.com/show_weidashang_pro/8565"
            },
            "options": {
                "total": true, //是否显示支持者的累积金额
                "rank": true, //是否显示支持者的排名
                "top": true //是否显示top排名
            }
        }
    ]
}
```
## 其他

提供代挂等服务，联系QQ407190960

安利一发，欢迎关注 [@BEJ48-刘胜男](http://weibo.com/u/5886797095)，群号548718867