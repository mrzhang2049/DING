import os
import math
import json
import random
import smtplib
import requests
import datetime
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 设置发件人、收件人、主题和正文
from_address = 'hellozhangxf@qq.com'
to_address = 'hellozhangxf@qq.com'
subject = 'Example HTML Email'

html_content = """
<html>
    <body>
        <h1>Hello, World!</h1>
        <p>This is an example of a HTML email.</p>
        <img src='https://img2023.cnblogs.com/blog/35695/202311/35695-20231130184233118-1375106894.jpg'>
    </body>
</html>
"""
# 获取天气和温度
def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


# 每日一句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)
def send_html_email(sender, receiver, subject, html_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # 将HTML内容转换为MIMEText对象，并设置其 subtype 为 'html'
    part = MIMEText(html_content, 'html')
    # 添加MIMEText对象到MIMEMultipart对象
    msg.attach(part)

    # 设置SMTP服务器地址、端口和登录凭据
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    username = "hellozhangxf@qq.com"
    password = "banwshuwomewdebi"
    try:
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp.login(username, password)
        smtp.sendmail(from_address, to_address, msg.as_string())
        print('发送成功')
    except:
        print('发送失败')


def send_msg(token_dd, msg, at_all=False):
    """
    通过钉钉机器人发送内容
    @param date_str:
    @param msg:
    @param at_all:
    @return:
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token_dd
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    content_str = "早上好！\n\n{0}\n".format(msg)

    data = {
        "msgtype": "text",
        "text": {
            "content": content_str
        },
        "at": {
            "isAtAll": at_all
        },
    }
    data = {
        "actionCard": {
            "title": "测试",
            "text": "测试",
            "btnOrientation": "0",
            "singleTitle": "测试",
            "singleURL": "https://www.dingtalk.com/"
        },
        "msgtype": "actionCard"
    }

    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=dd9371044f8fa37f87d0e2d6aa7779e9e0fe5726fa37d512d07c153829a526ab'
    secret = 'SEC85ac2fe0afe69b9d7b74ab53e9858521247477bfa564668a98eac07ae4d5344e'  # 可选：创建机器人勾选“加签”选项时使用
    xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
    #xiaoding.send_link(title='万万没想到，李小璐竟然...', text='故事是这样子的...', message_url='http://www.kwongwah.com.my/?p=454748", pic_url="https://pbs.twimg.com/media/CEwj7EDWgAE5eIF.jpg')
    xiaoding.send_text(msg='我就是小丁，小丁就是我！', is_at_all=False)
if __name__ == '__main__':
    token_dd = 'dd9371044f8fa37f87d0e2d6aa7779e9e0fe5726fa37d512d07c153829a526ab'
    city = "北京"
    # token_dd = '你自己的webhook后面的access_token复制在此'
    wea, temperature =('极冷',-200)
    note_str = "当前城市：{0}\n今日天气：{1}\n当前温度：{2}\n{3}".format(city, wea, temperature, get_words())
   # send_msg(token_dd, note_str, True)
    send_html_email(from_address, to_address, subject, html_content)

