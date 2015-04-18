QQ停放(自动回复)
=========  
[![Build Status](https://travis-ci.org/zeruniverse/QQParking.svg)](https://travis-ci.org/zeruniverse/QQParking)    
***该项目修改自[QQRobot](https://github.com/zeruniverse/QQRobot)这一项目***，用于挂QQ  
当收到私聊或临时对话时先回复离开信息，接下来由AI与用户聊天。

登陆时采用QQ安全中心的二维码做为登陆条件, 不需要在程序里输入QQ号码及QQ密码。

##如何使用
+ 从http://www.tuling123.com/openapi/ 申请一个API KEY(免费，5000次/天)， 贴到```QQBot.py```的第34行
+ ```nohup python2 QQBot.py >qbot.log&```
+ ```ls```
+ 若出现v.jpg则用QQ安全中心扫描，否则继续```ls```。
+ ```cat log.log```可以输出运行LOG



##功能

+ 私聊自动回复，某QQ号第一次触发私聊时回复离开信息

+ 私聊智能回复，小黄鸡，对于接下来收到的私聊，由机器人向AI平台请求该聊天记录的回复并回复给消息发送者

+ 私聊记录功能，以!!开头的信息记录LOG （待开发）


##TODO

+ ~~记录LOG~~(好像邮件提醒更科学）
