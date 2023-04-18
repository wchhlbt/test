import time
import datetime
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import requests
import time
# import socks
# import socket

# socks5 猴子补丁
# socks.set_default_proxy(socks.SOCKS5, "86.102.177.183", 1080)
# socket.socket = socks.socksocket
# # socks.set_default_proxy(socks.SOCKS5, "resi.zishon.net", 42324, username="wchhlbtme", password="k06b04of")
# # socks.set_default_proxy(socks.HTTP, "resi.zishon.net", 12321, username="wchhlbtme", password="k06b04of")

# # socks.set_default_proxy(socks.SOCKS5, "proxy.ipipgo.com", 31212, username="customer-6e9fef", password="e3ca87b6")
# # socks.set_default_proxy(socks.SOCKS5, "geo.iproyal.com", 42324, username="wchhlbt", password="1234abcd")
# # # socks.set_default_proxy(socks.SOCKS5, "localhost", 7891)


import dns.resolver

def get_email_domain(email):
    at_pos = email.find("@")
    if at_pos == -1:
        log("from_email format is invalid")
        return None
    return email[at_pos+1:]

def get_mx(domain):
    try:
        for x in dns.resolver.query(domain, 'MX'):
            txt = x.to_text()
            records = txt.split(" ")
            return records[len(records)-1]
    except:
        return None

# mailto_list = ['hellon123@protonmail.com']
mailto_list = ['security@mail1.nospoofing.cn']
# test-mibyop5vl@srv1.mail-tester.com
# mailto_list=['test-mibyop5vl@srv1.mail-tester.com']    #收件人(列表)
# mailto_list=['wch22@mails.tsinghua.edu.cn']    #收件人(列表)
rcpt_to = mailto_list[0]
mail_postfix = get_email_domain(rcpt_to)             #邮箱的后缀，网易就是163.com
# mail_host = get_mx(mail_postfix)
mail_host = 'a.nospoofing.cn'
print("=====",mail_host,"=========\n")

subject = "Thank you for shepherding the USENIX paper"
content = """
We carry out the first in-depth characterization of residential proxies (RESIPs) in China, for which little is studied in previous works. Our study is made possible through a semantic-based clas- sifier to automatically capture RESIP services. In addition to the classifier, new techniques have also been identified to capture RE- SIPs without interacting with and relaying traffic through RESIP services, which can significantly lower the cost and thus allow a continuous monitoring of RESIPs. Our RESIP service classifier has achieved a good performance with a recall of 99.7% and a preci- sion of 97.6% in 10-fold cross validation. Applying the classifier has identified 399 RESIP services, a much larger set compared to 38 RESIP services collected in all previous works. Our effort of RE- SIP capturing lead to a collection of 9,077,278 RESIP IPs (51.36% are located in China), 96.70% of which are not covered in publicly available RESIP datasets. An extensive measurement on RESIPs and their services has uncovered a set of interesting findings as well as several security implications. Especially, 80.05% RESIP IPs located in China have sourced at least one malicious traffic flows during 2021, resulting in 52-million malicious traffic flows in to- tal. And RESIPs have also been observed in corporation networks of 559 sensitive organizations including government agencies, ed- ucation institutions and enterprises. Also, 3,232,698 China RESIP IPs have opened at least one TCP/UDP ports for accepting relay- ing requests, which incurs non-negligible security risks to the local network of RESIPs. Besides, 91% China RESIP IPs are of a lifetime less than 10 days while most China RESIP services show up a crest- trough pattern in terms of the daily active RESIPs across time.
"""

source = 'Github'

def send_mail(from_domain, to_list):
    server = smtplib.SMTP()
    server.set_debuglevel(1)                        #打印出和SMTP服务器交互的所有信息
    server.connect(mail_host)                       #连接服务器
    server.helo(from_domain)
    
    mime_from = 'admin@' + from_domain
    me = mime_from
    msg = MIMEText(content, _subtype='plain')
    subject = "This is an email from {domain} via {source} from 25 port!".format(domain = from_domain, source = source)
    msg['Subject'] = subject
    # msg['From'] = ('%s<admin@139.com>' % Header("王楚涵","utf-8"))
    msg['From'] = mime_from
    msg['To'] = ";".join(to_list)                       #将收件人列表以‘；’分隔
    msg["Date"] = formatdate(localtime=True)
    msg['Sender'] = mime_from
    msg['Return-Path'] = mime_from
    try:        
        server.sendmail(me, to_list, msg.as_string())
    except Exception:
        print ("Error!")

    server.close()
    return

    
def check_and_send_email():
    burp0_url = "http://202.112.51.56:31247/check?m=cloudip"
    burp0_headers = {"Pragma": "no-cache", "Cache-Control": "no-cache", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7", "Connection": "close"}
    r = requests.get(burp0_url, headers=burp0_headers)
    print(r.text)
    ans = json.loads(r.text)
    
    # choose the shortest domain to show the result
    domain_list = ans['domains']
    domain_list = domain_list.split()
    minlen = len(domain_list[0])
    from_domain = domain_list[0]
    for domain in domain_list:
        if len(domain) < minlen:
            minlen = len(domain)
            from_domain = domain

    if ans['status'] == 'True':
        print("yes")
        send_mail('dgs.virginia.com', mailto_list)
        # send_mail('polycom.com', mailto_list)
        # send_mail(from_domain, mailto_list)
    else:
        print("false")

# send_mail('nark.ru', mailto_list)
check_and_send_email()


