import os
import math
import json
import random
import time
import smtplib
import requests
import datetime
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from vika import Vika

from_address = 'hellozhangxf@qq.com'
to_address = 'hellozhangxf@qq.com'
subject = '小伙刮中100万拔腿就跑了'


def send_msg():
    # 设置SMTP服务器地址、端口和登录凭据
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    username = "hellozhangxf@qq.com"
    password = "banwshuwomewdebi"
    # 模板路径
    template_path = 'email_template3.html'

    # 模板参数
    template_vars = {
        'name': 'John Doe',
        'trendimg3': 'https://j4.dfcfw.com/charts/pic6/159925.png',
        'trendimg': 'http://j3.dfcfw.com/images/JJJZ1/159925.png',
        'users': [
            {'name': 'Alice', 'email': 'alice@example.com', 'age': 30},
            {'name': 'Bob', 'email': 'bob@example.com', 'age': 25},
            {'name': 'Charlie', 'email': 'charlie@example.com', 'age': 28},
        ],
    }
    # 读取模板文件
    with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
        template_text = f.read()
    # 使用 Jinja2 渲染模板
    template = Template(template_text)
    html_content = template.render(template_vars)
    # 创建MIMEMultipart对象，并设置必要的属性
    msg = MIMEMultipart('alternative')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    # 将正文设置为一个MIMEText对象，其中subtype参数被设为'html'以表示它是HTML内容
    msg.attach(MIMEText(html_content, 'html'))
    # 设置SMTP服务器地址、端口和登录凭据
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    username = "hellozhangxf@qq.com"
    password = "banwshuwomewdebi"
    try:
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp.login(username, password)
        #smtp.sendmail(from_address, to_address, msg.as_string())
        print('发送成功')
    except:
        print('发送失败')
if __name__ == '__main__':
    send_msg()
    vika = Vika("uskKX37HkZuodf8VkY7CiQ1")
    # 通过 datasheetId 来指定要从哪张维格表操作数据。
    datasheet = vika.datasheet("dst1CSXS5xqdZJHTLZ", field_key="name")
    list = datasheet.records.filter(Name="QWE33")
    time.sleep(10)
    if list.count()==0:
        records = datasheet.records.bulk_create([
            {
                "Name": "QWE33",
                "Code": "10902",
                "StartDate": 1698854400000,
                "StartValue": 1.09,
                "CurrentValue": 1.2
            },
            {
                "Name": "QW",
                "Code": "10902",
                "StartDate": 1698854400000,
                "StartValue": 1.09,
                "CurrentValue": 1.2
            }
        ])
    else:
        print(list)
        row = list.first()
        _file = datasheet.upload_file('https://cdn.nlark.com/yuque/0/2023/png/12406411/1687853326261-51894522-7b39-4bca-b83a-e8bd60eab30a.png')
        time.sleep(2)
        row.Image = [_file]
        time.sleep(2)
        # 创建单条记录
        row.update({
            "Name": "HelloZhang",
            "Code": "902",
            "StartDate": 1698854400000,
            "StartValue": 1.09,
            "CurrentValue": 1.2,
        })




