# encoding=utf-8
import random
import time
from datetime import datetime

import efinance as ef
import requests
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
            baseinfo = ef.fund.get_base_info(item.strip())
            filter = {"property": "Code", "rich_text": {"contains": f'{item}'}}
            query_result = notion.databases.query(database_id=database_id, filter=filter).get("results")
            length = len(query_result)
            if length == 0:
                new_page = {
                    "Code": {"title": [{"type": "text", "text": {"content": baseinfo['基金代码']}}]},
                    "Name": {"rich_text": [{"type": "text", "text": {"content": baseinfo['基金简称']}}]},
                    "StartDate": {'type': 'date', 'date': {'start': str(baseinfo['净值更新日期']), 'end': None}},
                    'StartVal': {'type': 'number', 'number': double(baseinfo['最新净值'])},
                    'CurrentVal': {'type': 'number', 'number': double(baseinfo['最新净值'])},
                    "File": {"files": [{"type": "external", "name": "Cover",
                                        "external": {
                                            "url": f"https://j3.dfcfw.com/images/APPFavorNav/big/SYL_3Y/{baseinfo['基金代码']}.png"}}]}
                }
                notion.pages.create(parent=parent, properties=new_page)
                # send_dingtalk(item[0])
            else:
                for ite in query_result:
                    page_id = ite['id']
                    new_page = {
                        'CurrentVal': {'type': 'number', 'number': double(baseinfo['最新净值'])},
                    }
                    #TODO:提醒推送
                    res= notion.pages.update(page_id=page_id, properties=new_page)

