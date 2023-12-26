import sys
import random
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime
import time
from notion_client import Client
from_address = 'hellozhangxf@qq.com'
to_address = 'hellozhangxf@qq.com'
subject = '小伙刮中100了'


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
        # smtp.sendmail(from_address, to_address, msg.as_string())
        print('发送成功')
    except:
        print('发送失败')


def send_dingtalk(msg):
    """
        @param date_str:
        @param msg:
        @param at_all:
        @return:
        """
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=dd9371044f8fa37f87d0e2d6aa7779e9e0fe5726fa37d512d07c153829a526ab'
    secret = 'SEC85ac2fe0afe69b9d7b74ab53e9858521247477bfa564668a98eac07ae4d5344e'
    xiaoding = DingtalkChatbot(webhook, secret=secret)
    xiaoding.send_text(msg, is_at_all=False)


if __name__ == '__main__':
    num = (int)(sys.argv[1])
    database_id = '61b85174dbb64557ae4721104bc267ab'
    notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
    notion = Client(auth=notion_token)
    parent = {"database_id": database_id, "type": "database_id"}
    # vika = Vika("uskKX37HkZuodf8VkY7CiQ1")
    # 通过 datasheetId 来指定要从哪张维格表操作数据。
    # datasheet = vika.datasheet("dst1CSXS5xqdZJHTLZ", field_key="name")
    i = (num - 1) * 8
    time.sleep(5)
    session = requests.session()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'./document_{current_date}.txt'
    with open(filename, 'w+') as file:
        file.write(datetime.now().strftime('%Y-%m-%d'))
    while num * 8 >= i >= (num - 1) * 8:
        i = i + 1
        headers = {
            'X-Forwarded-For': f'{random.randint(10, 126)}.{random.randint(10, 254)}.{random.randint(10, 254)}.{random.randint(10, 254)}'
        }
        url = f'https://api-ddc-wscn.awtmt.com/market/rank?market_type=mdc&stk_type=stock&order_by=none&sort_field=px_change_rate&limit=15&fields=prod_name%2Cprod_en_name%2Cprod_code%2Csymbol%2Clast_px%2Cpx_change%2Cpx_change_rate%2Chigh_px%2Clow_px%2Cweek_52_high%2Cweek_52_low%2Cprice_precision%2Cupdate_time&cursor={i}';
        print(url)
        res = session.get(url, headers=headers).json()
        datalist = res['data']['candle']
        for item in datalist:
            time.sleep(3)
            if item[10] == item[8]:
                new_page = {
                    "Name": {"title": [{"text": {"content": f'{item[0]}'}}]},
                    "Tags": {"type": "multi_select", "multi_select": [{"name": f'{i}'}]},
                    "Cover": {"files": [{"type": "external", "name": "Cover",
                                         "external": {
                                             "url": "https://gw.alipayobjects.com/zos/bmw-prod/1c363c0b-17c6-4b00-881a-bc774df1ebeb.svg"}}]}
                }
                notion.pages.create(parent=parent, properties=new_page)
                send_dingtalk(item[0])
