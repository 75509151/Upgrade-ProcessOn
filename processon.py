from concurrent.futures import ThreadPoolExecutor
import random
import re
import time
import sys

import requests
from bs4 import BeautifulSoup
from captcha import Crack



domains = []
count = 0
logpath = r'D:\Upgrade-ProcessOn\log.txt'

def log_file(log):
    file = open(logpath, 'w', encoding='utf-8')
    file.write(log)
    file.close()


def getuser():

    user = str(random.randint(1000000, 9999999))

    return user


def getdomain():
    global domains
    if domains == []:
        r = requests.get("https://temp-mail.org/en/option/change/")
        soup = BeautifulSoup(r.text, "html.parser")
        domains = [tag.text for tag in soup.find(id="domain").find_all("option")]
    return random.choice(domains)


def po(user, domain, url):
    fullname = str(random.randint(1000000, 9999999))
    password = str(random.randint(1000000, 9999999))
    # url, email, psw, name
    print(url, password, fullname)
    crack = Crack(url, user + domain, password, fullname)
    crack.open()

    fmt = "\nemail: {}"
    print(fmt.format(user + domain))
    return crack


def mail(user, domain):
    global count

    ss_mail = requests.Session()
    rsp_get = ss_mail.get("https://temp-mail.org/zh/option/change/")
    csrf = re.findall(r'name="csrf" value="(\w+)', rsp_get.text)[0]

    tempmail = {"csrf": csrf, "mail": user, "domain": domain}

    ss_mail.post("https://temp-mail.org/zh/option/change/", data=tempmail)

    rsp_refresh = ss_mail.get("https://temp-mail.org/zh/option/refresh/")
    url_box = re.findall(r"https://temp-mail.org/zh/view/\w+", rsp_refresh.text)
    while url_box == []:
        time.sleep(1)
        rsp_refresh = ss_mail.get("https://temp-mail.org/zh/option/refresh/")
        url_box = re.findall(r"https://temp-mail.org/zh/view/\w+", rsp_refresh.text)

    rsp_message = ss_mail.get(url_box[0])
    #log_file(rsp_message.text)
    url_verify = re.findall(
        #r"https://www.processon.com/signup/verification/\w+", rsp_message.text
        r'>(\w+)</strong>', rsp_message.text
    )
    print(url_verify)
    ss_mail.post("https://temp-mail.org/zh/option/delete/", data=tempmail)
    return url_verify[0]



def make(user):
    domain = getdomain()
    crack = po(user, domain, url)
    verify_code = mail(user, domain)
    crack.submit(verify_code)


if __name__ == "__main__":
    # url = "https://www.processon.com/i/5ad16f4be4b0518eacae31fb"
    url = input("请输入你的邀请链接：")
    for i in range(10):
        make(getuser())