QQ停放(自动回复)
=========  
[![Build Status](https://travis-ci.org/zeruniverse/QQParking.svg)](https://travis-ci.org/zeruniverse/QQParking)
[![Code Health](https://landscape.io/github/zeruniverse/QQParking/master/landscape.svg?style=flat)](https://landscape.io/github/zeruniverse/QQParking/master)
![Release](https://img.shields.io/github/release/zeruniverse/QQParking.svg)
![Environment](https://img.shields.io/badge/python-2.6, 2.7-blue.svg)
![License](https://img.shields.io/github/license/zeruniverse/QQParking.svg)      
***该项目修改自[QQRobot](https://github.com/zeruniverse/QQRobot)这一项目***，用于挂QQ  
当收到私聊或临时对话时先回复离开信息，接下来由AI与用户聊天。记录用户发送的留言并邮件提醒  
点[这里](https://github.com/zeruniverse/QQParking/releases/tag/2.3)可以下载不带邮件功能的版本。  
登陆时采用QQ安全中心的二维码做为登陆条件, 不需要在程序里输入QQ号码及QQ密码。   
  
**请帮忙分析Android QQ协议**：此项目现已稳定，在更新协议前不会有大更新。希望有人能跟我一起搞手机QQ协议，SmartQQ协议稳定性不是很理想。  
  
This project is a chatting robot in QQ, implemented in Python. The purpose of this project is keeping your QQ account online 24*7. This robot will ignore all group chatting messages and reply to each private chatting message. The robot will first tell people chatting with your account that you're not online and an AI robot will chat with them on behalf of you. If they want to leave a message to you, they can send [record] command in chatting window and the next message will be forwarded to your electronic mailbox. The welcome message will be sent at the first time the robot reply to a certain account and every following message will end up with (This message is sent from an robot).  

[Here](https://github.com/zeruniverse/QQRobot) is a similar project supporting both group chatting and private chatting but only used for fun.  

##运行截图  
<img width="533" alt="capture" src="https://cloud.githubusercontent.com/assets/4648756/9015609/ee46e016-377e-11e5-83c7-9346d811a664.PNG">  
<img width="534" alt="capture1" src="https://cloud.githubusercontent.com/assets/4648756/9015624/fd96946c-377e-11e5-980d-a50f6aa5b663.PNG">  
执行上一步后收到留言邮件提示：  
<img width="526" alt="capture3" src="https://cloud.githubusercontent.com/assets/4648756/9015639/129bc832-377f-11e5-90d0-f73a7f0a2c33.PNG">  
小黄鸡代聊：  
<img width="538" alt="capture4" src="https://cloud.githubusercontent.com/assets/4648756/9015657/37f5db90-377f-11e5-82dc-310b53fe17e4.PNG">  
QQ下线需要重新登录提醒：  
<img width="649" alt="capture5" src="https://cloud.githubusercontent.com/assets/4648756/9015668/4a1612cc-377f-11e5-9903-07bbebfc9a0d.PNG">  
（对应错误）  
<img width="483" alt="capture6" src="https://cloud.githubusercontent.com/assets/4648756/9015680/624ed478-377f-11e5-893a-3dea56d8efe9.PNG">  
  
##RELEASE    
5.1挂机版本 (带预配置文件)：[点击下载](https://github.com/zeruniverse/QQParking/releases/tag/5.1)  
~~5.0.1 WINDOWS EXE 32位: [点击下载](https://github.com/zeruniverse/QQParking/releases/tag/w5.0.1)~~  
~~无邮件提醒功能版本 (带预配置文件，可直接运行)： [点击下载](https://github.com/zeruniverse/QQParking/releases/tag/2.3)~~  
  
##如何使用
+ 从http://www.tuling123.com/openapi/ 申请一个API KEY(免费，5000次/天)
+ 将QQBot.py的第36-43行改为你的参数。接收邮箱请使用你的常用邮箱，发送邮箱建议网易126邮箱（已测试可用）,输入用户名，密码及对应SMTP服务器  
+ 如果您使用126邮箱，请在126邮箱-设置中开启smtp，并将SMTP专用密码（不是登陆密码）输入程序。开启smtp需要手机验证
+ ```nohup python2 QQBot.py >qbot.log&```
+ ```ls```
+ 若出现v.png则用QQ安全中心扫描，否则继续```ls```。
+ ```cat log.log```可以输出运行LOG
+ 测试用 API KEY 和邮箱：  
Tuling Key：c7c5abbc9ec9cad3a63bde71d17e3c2c  
邮箱： qqparking@126.com   
SMTP密码： uyyxdrzrrxntidkh  
邮箱和TULING KEY登陆密码：kidAi%u2^JSP9*.x  
TULING KEY 注册邮箱：qqparking@126.com  

##功能

+ 私聊自动回复，某QQ号第一次触发私聊时回复离开信息

+ 私聊智能回复，小黄鸡，对于接下来收到的私聊，由机器人向AI平台请求该聊天记录的回复并回复给消息发送者

+ 私聊记录功能，以record关键字触发重要信息记录，下一条信息将邮件提醒  

+ 留言失败提示，若留言邮件发送失败，则QQ上提醒对方重试  

+ 下线提示功能，若程序遇到错误退出（如QQ要求重新登录），则发送提醒邮件  
  



##其它

+ ~~如果需要不带邮件提示功能的版本，请下载这个: https://github.com/zeruniverse/QQParking/releases/tag/2.3~~  

+ 如果需要能够支持群聊的小黄鸡，请下载这个: https://github.com/zeruniverse/QQRobot

+ QQ协议参考自：[Yinzo](https://github.com/Yinzo/SmartQQBot) & [xqin](https://github.com/xqin/SmartQQ-for-Raspberry-Pi) 
