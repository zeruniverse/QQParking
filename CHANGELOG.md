#2015-04-16  
+ Only deal with PM (message or temp session)  
+ First reply leaving message, then reply content from AI platform  
+ need to add features: 1. record message {for message start with !!!, record it}  
+ fix wrap error  
+ log AI reply  
+ 发消息失败重试（最多三次）  
+ 若离开消息发送不成功，则杀死线程，防止小黄鸡莫名其妙出现  
  
#2015-04-17  
+ 把离开消息的发送和Logging从```__init__```移到```run()```防止进程添加进进程队列的过程太慢使进程重复生成
