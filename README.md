QQ停放(自动回复)
=========  
[![Build Status](https://travis-ci.org/zeruniverse/QQParking.svg)](https://travis-ci.org/zeruniverse/QQParking)    
***该项目修改自[QQRobot](https://github.com/zeruniverse/QQRobot)这一项目***，用于挂QQ  
当收到私聊或临时对话时先回复离开信息，接下来由AI与用户聊天。记录用户发送的留言并邮件提醒  
点[这里](https://github.com/zeruniverse/QQParking/releases/tag/2.3)可以下载不带邮件功能的版本。  
登陆时采用QQ安全中心的二维码做为登陆条件, 不需要在程序里输入QQ号码及QQ密码。  

##如何使用
+ 从http://www.tuling123.com/openapi/ 申请一个API KEY(免费，5000次/天)
+ 将QQBot.py的第36-43行改为你的参数。接收邮箱请使用你的常用邮箱，发送邮箱建议网易126邮箱（已测试可用）,输入用户名，密码及对应SMTP服务器  
+ ```nohup python2 QQBot.py >qbot.log&```
+ ```ls```
+ 若出现v.jpg则用QQ安全中心扫描，否则继续```ls```。
+ ```cat log.log```可以输出运行LOG


##功能

+ 私聊自动回复，某QQ号第一次触发私聊时回复离开信息

+ 私聊智能回复，小黄鸡，对于接下来收到的私聊，由机器人向AI平台请求该聊天记录的回复并回复给消息发送者

+ 私聊记录功能，以!record开头的信息触发重要信息记录，下一条信息将邮件提醒  



##其它

+ 如果需要不带邮件提示功能的版本，请下载这个: https://github.com/zeruniverse/QQParking/releases/tag/2.3  

+ 如果需要能够支持群聊的小黄鸡，请下载这个: https://github.com/zeruniverse/QQRobot

+ QQ协议参考自：[Yinzo](https://github.com/Yinzo/SmartQQBot) & [xqin](https://github.com/xqin/SmartQQ-for-Raspberry-Pi) 
