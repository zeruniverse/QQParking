# -*- coding: utf-8 -*-

import re
import random
import json
import os
import sys
import datetime
import time
import threading
import logging
import urllib
import smtplib
from HttpClient import HttpClient
from email.Header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

reload(sys)
sys.setdefaultencoding("utf-8")

#SET YOUR OWN PARAMETERS HERE
tulingkey = '#YOUR KEY HERE'
mailserver = 'your smtp server, port 25(no encryption). e.g.:smtp.126.com'
mailsig = 'sender signiture, e.g.:QQParking Notification'
mailuser = 'your mail address of sender: e.g.:sender@126.com'
mailpass = 'sender mail password (to login to smtp server)'
sendtomail = '#send to which mail box. e.g.: recv@gmail.com'
#-----END OF SECTION-------

HttpClient_Ist = HttpClient()

ClientID = 53999199
PTWebQQ = ''
APPID = 0
msgId = 0
ThreadList = []
MailThreadList = []
PSessionID = ''

Referer = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
httpsReferer = 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1'
SmartQQUrl = 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'


VFWebQQ = ''
AdminQQ = '0'

#My QQ
MyUIN = 0
QQUserName = ''
#Put UserNameList Here to avoid multiple requests
MarkNameList = []
NickNameList = []
GroupList = []
DiscussionList = []

initTime = time.time()


logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

# -----------------
# 方法声明
# -----------------

#Encryption Algorithm Used By QQ
def gethash(selfuin, ptwebqq):
    selfuin += ""
    N=[0,0,0,0]
    for T in range(len(ptwebqq)):
        N[T%4]=N[T%4]^ord(ptwebqq[T])
    U=["EC","OK"]
    V=[0, 0, 0, 0]
    V[0]=int(selfuin) >> 24 & 255 ^ ord(U[0][0])
    V[1]=int(selfuin) >> 16 & 255 ^ ord(U[0][1])
    V[2]=int(selfuin) >>  8 & 255 ^ ord(U[1][0])
    V[3]=int(selfuin)       & 255 ^ ord(U[1][1])
    U=[0,0,0,0,0,0,0,0]
    U[0]=N[0]
    U[1]=V[0]
    U[2]=N[1]
    U[3]=V[1]
    U[4]=N[2]
    U[5]=V[2]
    U[6]=N[3]
    U[7]=V[3]
    N=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    V=""
    for T in range(len(U)):
        V+= N[ U[T]>>4 & 15]
        V+= N[ U[T]    & 15]
    return V

def get_ts():
    ts = time.time()
    while ts < 1000000000000:
        ts = ts * 10
    ts = int(ts)
    return ts

def CProcess(content):
    return str(content.replace("\\", r"\\").replace("\n", r"\n").replace("\r", r"\r").replace("\t", r"\t").replace('"', r'\"'))

def getQRtoken(qrsig):
    e = 0
    for i in qrsig:
        e += (e << 5) + ord(i)
    return 2147483647 & e;

def pass_time():
    global initTime
    rs = (time.time() - initTime)
    initTime = time.time()
    return str(round(rs, 3))


def getReValue(html, rex, er, ex):
    v = re.search(rex, html)

    if v is None:
        logging.error(er)

        if ex:
            raise Exception, er
        return ''

    return v.group(1)

def sendfailmail():
    global QQUserName, MyUIN
    try:
        SUBJECT = 'QQ挂机下线提醒： '+str(QQUserName)+'[QQ号：'+str(MyUIN)+']'
        TO = [sendtomail]
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(SUBJECT, 'utf-8')
        msg['From'] = mailsig+'<'+mailuser+'>'
        msg['To'] = ', '.join(TO)
        part = MIMEText("Fatal error occured. Please restart the program and login again!", 'plain', 'utf-8')
        msg.attach(part)
        server = smtplib.SMTP(mailserver, 25)
        server.login(mailuser, mailpass)
        server.login(mailuser, mailpass)
        server.sendmail(mailuser, TO, msg.as_string())
        server.quit()
        return True
    except Exception , e:
        logging.error("发送程序错误邮件失败:"+str(e))
        return False
def date_to_millis(d):
    return int(time.mktime(d.timetuple())) * 1000

def msg_handler(msgObj):
    for msg in msgObj:
        msgType = msg['poll_type']

        # QQ私聊消息
        if msgType == 'message' or msgType == 'sess_message':  # 私聊 or 临时对话
            txt = combine_msg(msg['value']['content'])
            tuin = msg['value']['from_uin']
            msg_id = msg['value']['msg_id']

            # print "{0}:{1}".format(from_account, txt)
            thread_cleanup()
            targetThread = thread_exist(tuin)
            if targetThread:
                targetThread.push(txt, msg_id)
            else:
                try:
                    service_type = 0
                    isSess = 0
                    group_sig = ''
                    myid = ''
                    if msgType == 'sess_message':
                        isSess = 1
                        service_type = msg['value']['service_type']
                        myid = msg['value']['id']
                        info = json.loads(HttpClient_Ist.Get('http://d1.web2.qq.com/channel/get_c2cmsg_sig2?id={0}&to_uin={1}&clientid={2}&psessionid={3}&service_type={4}&t={5}'.format(myid, tuin, ClientID, PSessionID, service_type, get_ts()), Referer))
                        logging.info("Get group sig:" + str(info))
                        if info['retcode'] != 0:
                            raise ValueError, info
                        info = info['result']
                        group_sig = info['value']
                    tmpThread = pmchat_thread(tuin,isSess,group_sig,service_type,txt,msg_id,myid)
                    tmpThread.start()
                    ThreadList.append(tmpThread)
                    logging.info("add thread "+str(tmpThread)+" for qq"+str(tuin))
                except Exception, e:
                    logging.info("error"+str(e))

            # print "{0}:{1}".format(self.FriendList.get(tuin, 0), txt)

            # if FriendList.get(tuin, 0) == AdminQQ:#如果消息的发送者与AdminQQ不相同, 则忽略本条消息不往下继续执行
            #     if txt[0] == '#':
            #         thread.start_new_thread(self.runCommand, (tuin, txt[1:].strip(), msgId))
            #         msgId += 1

            # if txt[0:4] == 'exit':
            #     logging.info(self.Get('http://d1.web2.qq.com/channel/logout2?ids=&clientid={0}&psessionid={1}'.format(self.ClientID, self.PSessionID), Referer))
            #     exit(0)

        # QQ号在另一个地方登陆, 被挤下线
        if msgType == 'kick_message':
            logging.error(msg['value']['reason'])
            raise Exception, msg['value']['reason']  # 抛出异常, 重新启动WebQQ, 需重新扫描QRCode来完成登陆


def combine_msg(content):
    msgTXT = ""
    for part in content:
        # print type(part)
        if type(part) == type(u'\u0000'):
            msgTXT += part
        elif len(part) > 1:
            # 如果是图片
            if str(part[0]) == "offpic" or str(part[0]) == "cface":
                msgTXT += "[图片]"

    return msgTXT


def send_msg(tuin, content, isSess, group_sig, service_type):
    if isSess == 0:
        reqURL = "https://d1.web2.qq.com/channel/send_buddy_msg2"
        data = (
            ('r', '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":{1}, "msg_id":{2}, "psessionid":"{3}"}}'.format(tuin, ClientID, msgId, PSessionID, CProcess(content))),
            ('clientid', ClientID),
            ('psessionid', PSessionID)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, httpsReferer)
        try:
            rspp = json.loads(rsp)
            if rspp['errCode']!= 0:
                logging.error("reply pmchat error"+str(rspp['errCode']))
                return False
            return True
        except:
            pass
    else:
        reqURL = "https://d1.web2.qq.com/channel/send_sess_msg2"
        data = (
            ('r', '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":{1}, "msg_id":{2}, "psessionid":"{3}", "group_sig":"{5}", "service_type":{6}}}'.format(tuin, ClientID, msgId, PSessionID, CProcess(content), group_sig, service_type)),
            ('clientid', ClientID),
            ('psessionid', PSessionID),
            ('group_sig', group_sig),
            ('service_type',service_type)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, httpsReferer)
        try:
            rspp = json.loads(rsp)
            if rspp['errCode']!= 0:
                logging.error("reply temp pmchat error"+str(rspp['errCode']))
                return False
            return True
        except:
            pass
    return False


def thread_exist(tuin):
    for t in ThreadList:
        if t.isAlive():
            if t.tuin == tuin:
                t.check()
                return t
    return False

def thread_cleanup():
    for t in ThreadList:
        if not t.isAlive():
            ThreadList.remove(t)
    for t in MailThreadList:
        if not t.isAlive():
            MailThreadList.remove(t)
    return True

class send_mail(threading.Thread):

    def __init__(self, uin, content):
        threading.Thread.__init__(self)
        self.content = content
        self.uin = uin
    def run(self):
        global MarkNameList,NickNameList
        try:
            flag=0
            for t in NickNameList:
                if str(t["uin"])==str(self.uin):
                    hisnick=t["nick"]
                    flag=1
                    break
            if flag==0:
                raise ValueError, "Unable to find nick name"
            for t in MarkNameList:
                if str(t["uin"])==str(self.uin):
                    hismark=t["markname"]
                    flag=2
                    break
            if flag==1:
                subinfo="昵称："+str(hisnick)
            else:
                subinfo=str(hismark)+"(昵称："+str(hisnick)+")"
            flag=0
            while not self.smtpmail(subinfo):
                flag = flag + 1
                if flag > 3:
                    raise ValueError, flag
                    break
            return True
        except Exception , e:
            self.failmsg()
            logging.error("error sending msg for :"+str(e)+" times (send fail reply now)")
            return False
    def smtpmail(self,subinfo):
        try:
            SUBJECT = '来自 '+subinfo+'的留言'
            TO = [sendtomail]
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(SUBJECT, 'utf-8')
            msg['From'] = mailsig+'<'+mailuser+'>'
            msg['To'] = ', '.join(TO)
            part = MIMEText(self.content, 'plain', 'utf-8')
            msg.attach(part)
            server = smtplib.SMTP(mailserver, 25)
            server.login(mailuser, mailpass)
            server.login(mailuser, mailpass)
            server.sendmail(mailuser, TO, msg.as_string())
            server.quit()
            return True
        except Exception, e:
            logging.error("error sending msg:"+str(e))
            return False
    def failmsg(self):
        targetThread = thread_exist(int(self.uin))
        logging.info("邮件发送失败提示，push进线程："+str(targetThread))
        if targetThread:
            targetThread.reply("抱歉，留言发送失败，留言内容为:\n"+str(self.content))
        return True

class send_sess_mail(threading.Thread):

    def __init__(self, uin, content, sess_group_id, service_type):
        threading.Thread.__init__(self)
        self.content = content
        self.uin = uin
        self.sess_group_id = sess_group_id
        self.service_type = service_type
    def run(self):
        try:
            subinfo,gcode,gname = self.get_display_name()
            SUBJECT = '来自（临时对话） '+subinfo+'的留言'
            if self.service_type == 0:
                SUBJECT = SUBJECT + "(来自群："+gname+")"
            else:
                SUBJECT = SUBJECT + "(来自讨论组："+gname+")"
            flag=1
            while not self.smtpmail(SUBJECT):
                flag = flag + 1
                if flag > 3:
                    raise ValueError, flag
                    break
            return True
        except Exception , e:
            self.failmsg()
            logging.error("error sending msg for :"+str(e)+" times (send fail reply now)")
            return False
    def smtpmail(self,SUBJECT):
        try:
            TO = [sendtomail]
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(SUBJECT, 'utf-8')
            msg['From'] = mailsig+'<'+mailuser+'>'
            msg['To'] = ', '.join(TO)
            part = MIMEText(self.content, 'plain', 'utf-8')
            msg.attach(part)
            server = smtplib.SMTP(mailserver, 25)
            server.login(mailuser, mailpass)
            server.login(mailuser, mailpass)
            server.sendmail(mailuser, TO, msg.as_string())
            server.quit()
            return True
        except Exception, e:
            logging.error("error sending msg:"+str(e))
            return False
    def get_display_name(self):
        global GroupList, DiscussionList
        #群临时对话
        flag=0
        if self.service_type == 0:
            for t in GroupList:
                if str(t["gid"])==str(self.sess_group_id):
                    group_name=t["name"]
                    group_code=t["code"]
                    flag=1
                    break
            if flag==0:
                raise ValueError, "Unable to find corresponding group"

            html = HttpClient_Ist.Get('http://s.web2.qq.com/api/get_group_info_ext2?gcode={0}&vfwebqq={1}&t={2}'.format(group_code, VFWebQQ,get_ts()), Referer)
            ret = json.loads(html)
            if ret['retcode']!= 0:
                raise ValueError, "retcode error when getting group detail info: retcode="+ret['retcode']
            flag=0
            for t in ret['result']['minfo']:
                if str(t["uin"])==str(self.uin):
                    hisnick=t["nick"]
                    flag=1
                    break
            if flag==0:
                raise ValueError, "Unable to find nick name in sess from_group"
            for t in ret['result']['cards']:
                if str(t["muin"])==str(self.uin):
                    hismark=t["card"]
                    flag=2
                    break
            if flag==1:
                subinfo="昵称："+str(hisnick)
            else:
                subinfo=str(hismark)+"(昵称："+str(hisnick)+")"
            return (subinfo,group_code,group_name)
        else:
            for t in DiscussionList:
                if str(t["did"])==str(self.sess_group_id):
                    group_name=t["name"]
                    flag=1
                    break
            if flag==0:
                raise ValueError, "Unable to find corresponding discussion group"

            html = HttpClient_Ist.Get('http://d1.web2.qq.com/channel/get_discu_info?did={0}&vfwebqq={1}&clientid={2}&psessionid={3}&t={4}'.format(self.sess_group_id, VFWebQQ, ClientID,PSessionID,get_ts()), Referer)
            ret = json.loads(html)
            if ret['retcode']!= 0:
                raise ValueError, "retcode error when getting discussion group detail info: retcode="+ret['retcode']
            flag=0
            for t in ret['result']['mem_info']:
                if str(t["uin"])==str(self.uin):
                    hisnick=t["nick"]
                    flag=1
                    break
            if flag==0:
                raise ValueError, "Unable to find nick name in sess from_discussion_group"
            subinfo="昵称："+str(hisnick)
            return (subinfo,self.sess_group_id,group_name)

    def failmsg(self):
        targetThread = thread_exist(int(self.uin))
        logging.info("邮件发送失败提示，push进线程："+str(targetThread))
        if targetThread:
            targetThread.reply("抱歉，留言发送失败，留言内容为:\n"+str(self.content))
        return True
# -----------------
# 类声明
# -----------------


class Login(HttpClient):
    MaxTryTime = 5

    def __init__(self, vpath, qq=0):
        global APPID, AdminQQ, PTWebQQ, VFWebQQ, PSessionID, msgId, MyUIN,MarkNameList,NickNameList,GroupList,DiscussionList,QQUserName
        self.VPath = vpath  # QRCode保存路径
        AdminQQ = int(qq)
        logging.critical("正在获取登陆页面")
        self.Get('http://w.qq.com/')
        html = self.Get(SmartQQUrl,'http://w.qq.com/')
        logging.critical("正在获取appid")
        APPID = getReValue(html, r'<input type="hidden" name="aid" value="(\d+)" />', 'Get AppId Error', 1)
        logging.critical("正在获取login_sig")
        sign = getReValue(html, r'g_login_sig\s*=\s*encodeURIComponent\s*\("(.*?)"\)', 'Get Login Sign Error', 0)
        logging.info('get sign : %s', sign)
        logging.critical("正在获取pt_version")
        JsVer = getReValue(html, r'g_pt_version\s*=\s*encodeURIComponent\s*\("(\d+)"\)', 'Get g_pt_version Error', 1)
        logging.info('get g_pt_version : %s', JsVer)
        logging.critical("正在获取mibao_css")
        MiBaoCss = getReValue(html, r'g_mibao_css\s*=\s*encodeURIComponent\s*\("(.*?)"\)', 'Get g_mibao_css Error', 1)
        logging.info('get g_mibao_css : %s', sign)
        StarTime = date_to_millis(datetime.datetime.utcnow())
        T = 0
        while True:
            T = T + 1
            self.Download('https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=M&s=5&d=72&v=4&t=0.0836106{1}4250{2}6653'.format(APPID,random.randint(0,9),random.randint(0,9)), self.VPath)

            logging.info('[{0}] Get QRCode Picture Success.'.format(T))

            QRSig = self.getCookie('qrsig')
            while True:
                html = self.Get('https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken={0}&webqq_type=10&remember_uin=1&login2qq=1&aid={1}&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{2}&mibao_css={3}&t=1&g=1&js_type=0&js_ver={4}&login_sig={5}&pt_randsalt=2'.format(getQRtoken(QRSig),APPID, date_to_millis(datetime.datetime.utcnow()) - StarTime, MiBaoCss, JsVer, sign),
                        SmartQQUrl)
                # logging.info(html)
                ret = html.split("'")
                if ret[1] == '65' or ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                    break
                time.sleep(2)
            if ret[1] == '0' or T > self.MaxTryTime:
                break

        logging.info(ret)
        if ret[1] != '0':
            raise ValueError, "RetCode = "+ret['retcode']
            return
        logging.critical("二维码已扫描，正在登陆")
        pass_time()
        # 删除QRCode文件
        if os.path.exists(self.VPath):
            os.remove(self.VPath)

        # 记录登陆账号的昵称
        tmpUserName = ret[11]

        html = self.Get(ret[5])
        url = getReValue(html, r' src="(.+?)"', 'Get mibao_res Url Error.', 0)
        if url != '':
            html = self.Get(url.replace('&amp;', '&'))
            url = getReValue(html, r'location\.href="(.+?)"', 'Get Redirect Url Error', 1)
            html = self.Get(url)

        PTWebQQ = self.getCookie('ptwebqq')

        logging.info('PTWebQQ: {0}'.format(PTWebQQ))

        LoginError = 3
        while LoginError > 0:
            try:
                html = self.Post('http://d1.web2.qq.com/channel/login2', {
                    'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(PTWebQQ, ClientID, PSessionID)
                }, 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2')
                ret = json.loads(html)
                html2 = self.Get("http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}".format(PTWebQQ, ClientID, PSessionID, get_ts()), Referer)
                logging.info("getvfwebqq html:  " + str(html2))
                ret2 = json.loads(html2)
                LoginError = 0
            except:
                LoginError -= 1
                logging.critical("登录失败，正在重试")

        if ret['retcode'] != 0 or ret2['retcode'] != 0:
            raise ValueError, "Login Retcode="+str(ret['retcode'])
            return

        VFWebQQ = ret2['result']['vfwebqq']
        PSessionID = ret['result']['psessionid']
        MyUIN = ret['result']['uin']
        logging.critical("QQ号：{0} 登陆成功, 用户名：{1}".format(ret['result']['uin'], tmpUserName))
        logging.info('Login success')
        logging.critical("登陆二维码用时" + pass_time() + "秒")
        QQUserName = tmpUserName
        msgId = int(random.uniform(20000, 50000))

        self.Get('http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={0}&clientid={1}&psessionid={2}&t={3}'.format(VFWebQQ,ClientID,PSessionID,get_ts()),Referer)

        html = self.Post('http://s.web2.qq.com/api/get_user_friends2', {
                'r': '{{"vfwebqq":"{0}","hash":"{1}"}}'.format(str(VFWebQQ),gethash(str(MyUIN),str(PTWebQQ)))
            }, Referer)
        ret = json.loads(html)
        if ret['retcode']!= 0:
            raise ValueError, "retcode error when getting friends list: retcode="+ret['retcode']
        NickNameList = ret['result']['info']
        MarkNameList = ret['result']['marknames']
        html = self.Get('http://s.web2.qq.com/api/get_discus_list?clientid={0}&psessionid={1}&vfwebqq={2}&t={3}'.format(ClientID, PSessionID, VFWebQQ,get_ts()), Referer)
        ret = json.loads(html)
        if ret['retcode']!= 0:
            raise ValueError, "retcode error when getting discussion group list: retcode="+ret['retcode']
        DiscussionList = ret['result']['dnamelist']
        html = self.Post('http://s.web2.qq.com/api/get_group_name_list_mask2', {
                'r': '{{"vfwebqq":"{0}","hash":"{1}"}}'.format(str(VFWebQQ),gethash(str(MyUIN),str(PTWebQQ)))
            }, Referer)
        ret = json.loads(html)
        if ret['retcode']!= 0:
            raise ValueError, "retcode error when getting group list: retcode="+str(ret['retcode'])
        GroupList = ret['result']['gnamelist']

class check_msg(threading.Thread):
    # try:
    #   pass
    # except KeybordInterrupt:
    #   try:
    #     user_input = (raw_input("回复系统：（输入格式:{群聊2or私聊1}, {群号or账号}, {内容}）\n")).split(",")
    #     if (user_input[0] == 1):

    #       for kv in self.FriendList :
    #         if str(kv[1]) == str(user_input[1]):
    #           tuin == kv[0]

    #       self.send_msg(tuin, user_input[2])

    #   except KeybordInterrupt:
    #     exit(0)
    #   except Exception, e:
    #     print Exception, e

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global PTWebQQ
        E = 0
        # 心跳包轮询
        while 1:
            if E > 5:
                break
            try:
                ret = self.check()
            except:
                E += 1
                continue
            # logging.info(ret)

            # 返回数据有误
            if ret == "":
                E += 1
                continue

            # POST数据有误
            if ret['retcode'] == 100006:
                break

            # 无消息
            if ret['retcode'] == 102:
                E = 0
                continue

            # 更新PTWebQQ值
            if ret['retcode'] == 116:
                PTWebQQ = ret['p']
                E = 0
                continue

            if ret['retcode'] == 0:
                # 信息分发
                if 'result' in ret:
                    msg_handler(ret['result'])
                E = 0
                continue

            # Exit on abnormal retcode
            E += 1
            HttpClient_Ist.Get('http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={0}&clientid={1}&psessionid={2}&t={3}'.format(VFWebQQ,ClientID,PSessionID,get_ts()),Referer)

        logging.critical("轮询错误超过五次")

    # 向服务器查询新消息
    def check(self):

        html = HttpClient_Ist.Post('https://d1.web2.qq.com/channel/poll2', {
            'r': '{{"ptwebqq":"{1}","clientid":{2},"psessionid":"{0}","key":""}}'.format(PSessionID, PTWebQQ, ClientID)
        }, httpsReferer)
        logging.info("Check html: " + str(html))
        try:
            ret = json.loads(html)
        except Exception as e:
            logging.error(str(e))
            logging.critical("Check error occured, retrying.")
            return self.check()

        return ret


class pmchat_thread(threading.Thread):


    # con = threading.Condition()
    autoreply = '最近需要认真学习，不上QQ,有事请邮件联系。接下来由小黄鸡代我与您聊天！在聊天时输入【record】可以开始给我留言，(英文单词: record），输入此命令并在收到提示后输入留言内容即可.record前面不能有空格（r需为该消息的第一个字符）'
    # newIp = ''

    def __init__(self, tuin, isSess, group_sig, service_type,ini_txt,ini_msgid,myid):
        threading.Thread.__init__(self)
        self.tuin = tuin
        self.isSess = isSess
        self.group_sig=group_sig
        self.service_type=service_type
        self.lastcheck = time.time()
        self.lastseq=0
        self.lastmail=0
        self.isrecord=0
        self.ini_txt=ini_txt
        self.ini_msgid=ini_msgid
        self.sess_group_id = myid
        self.replystreak = 0
    def check(self):
        self.lastcheck = time.time()
    def run(self):
        logging.info("私聊线程生成，私聊对象："+str(self.tuin))
        self.awaymsgsucc = self.reply(self.autoreply)
        self.push(self.ini_txt,self.ini_msgid)
        while self.awaymsgsucc:
            time.sleep(119)
            if time.time() - self.lastcheck > 800:
                break

    def reply(self, content):
        failtimes = 0
        while not send_msg(self.tuin, str(content)+"(此消息来自小黄鸡，非本人)", self.isSess, self.group_sig, self.service_type):
            failtimes = failtimes + 1
            if failtimes >= 3:
                break
            time.sleep(1)
        if failtimes < 3:
            logging.info("Reply to UIN " + str(self.tuin) + ":" + str(content))
            return True
        else:
            logging.error("FAIL TO Reply to UIN " + str(self.tuin) + ":" + str(content))
            return False
    def record_important(self, content):
        pattern = re.compile(r'^(record)')
        match = pattern.match(content)
        try:
            if match:
                if time.time() - self.lastmail < 300.0:
                    logging.info("EMAIL TOO FAST, ABANDON："+content)
                    self.reply("您留言太频繁了，请5分钟后重试！")
                    return True
                self.lastmail = time.time()
                logging.info("start recording important message")
                self.reply("请回复您需要留言的内容，请将所有内容合并在一条回复中（可分行）。您的昵称与备注名将自动被记录，请留下联系方式以便我回复您！")
                self.isrecord = 1
                return True
            return False
        except Exception, e:
            logging.error("ERROR"+str(e))
        return False
    def record(self, content):
        try:
            if self.isrecord==0:
                return False
            if self.isrecord==1:
                self.isrecord = 0
                if self.isSess == 0:
                    tmpthread = send_mail(str(self.tuin),str(content).decode('UTF-8'))
                else:
                    tmpthread = send_sess_mail(str(self.tuin),str(content).decode('UTF-8'),str(self.sess_group_id),self.service_type)
                tmpthread.start()
                MailThreadList.append(tmpthread)
                self.reply("此消息已记录，主人会尽快回复！记录的内容如下\n"+str(content))
                return True
            return False
        except Exception, e:
            logging.error("ERROR"+str(e))
        return False
    def push(self, ipContent, seq):
        if seq == self.lastseq:
            return True
        else:
            self.lastseq=seq

        try:
            if self.record(ipContent):
                return True
            if self.record_important(ipContent):
                return True
            self.replystreak = self.replystreak + 1
            #防止机器人对聊
            if self.replystreak>30:
                self.replystreak = 0
                return True
            logging.info("PM get info from AI: "+ipContent)
            paraf={ 'userid' : str(self.tuin), 'key' : tulingkey, 'info' : ipContent}
            info = HttpClient_Ist.Get('http://www.tuling123.com/openapi/api?'+urllib.urlencode(paraf))
            logging.info("AI REPLY:"+str(info))
            info = json.loads(info)
            if info["code"] in [40001, 40003, 40004]:
                self.reply("我今天累了，不聊了")
                logging.warning("Reach max AI call")
            elif info["code"] in [40002, 40005, 40006, 40007]:
                self.reply("我遇到了一点问题，请稍后@我")
                logging.warning("PM AI return error, code:"+str(info["code"]))
            else:
                rpy = str(info["text"]).replace('<主人>','你').replace('<br>',"\n")
                self.reply(rpy)
            return True
        except Exception, e:
            logging.error("ERROR:"+str(e))
        return False

# -----------------
# 主程序
# -----------------

if __name__ == "__main__":
    vpath = './v.png'
    qq = 0
    if len(sys.argv) > 1:
        vpath = sys.argv[1]
    if len(sys.argv) > 2:
        qq = sys.argv[2]

    try:
        pass_time()
        qqLogin = Login(vpath, qq)
    except Exception, e:
        logging.error(str(e))
        os._exit(1)
    try:
        t_check = check_msg()
        t_check.setDaemon(True)
        t_check.start()
        t_check.join()
    except:
        pass
    errortime=0
    logging.info("发送下线邮件...")
    while errortime<5:
        errortime=errortime+1
        if sendfailmail():
            break
