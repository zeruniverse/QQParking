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

#2015-04-22  
+ 腾讯是个坑，返回retcode=0消息不一定发送成功。为防止误会，给回复的每条内容加上小尾巴

#2015-04-26  
+ 增加邮件提醒  
  
#2015-04-27  
+ 解决编码问题导致的错误
+ 限制每5分钟留言一次防止邮箱被爆
+ 准备开新线程发邮件，不然容易卡住

#2015-04-28  
+ 发邮件新开进程避免卡死回复进程   
  
#2015-07-19    
+ 部分编码问题（换行符）  
  
#2015-07-20  
+ 优化邮件发送  

#2015-07-25  
+ 邮件发送增加昵称与备注名，临时对话群名和群名片   
+ 邮件发送失败提示留言方  
+ 错误退出发送邮件提醒重新登录
