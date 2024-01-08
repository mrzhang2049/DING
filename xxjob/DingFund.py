# encoding=utf-8
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
import efinance as ef
from notion_client import Client
from numpy import double

if __name__ == '__main__':
    database_id = '56641c6587cd400fb9037cf86a51d5d9'
    notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
    notion = Client(auth=notion_token)
    parent = {"database_id": database_id, "type": "database_id"}
    random_number = random.random()
    time.sleep(random_number)
    session = requests.session()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'./document_{current_date}.txt'
    with open('./txt_dingfund.txt', 'r') as file:
        for item in file:
            baseinfo=ef.fund.get_base_info(item.strip())

