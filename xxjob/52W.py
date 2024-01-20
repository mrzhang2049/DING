import random
import sys
from datetime import datetime

import httpx
from notion_client import Client

if __name__ == '__main__':
    num = (int)(sys.argv[1])
    database_id = '9b83664c12e443628f669752e55449aa'
    notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
    notion = Client(auth=notion_token)
    parent = {"database_id": database_id, "type": "database_id"}
    i = (num - 1) * 8
    # random_number = random.random()
    # time.sleep(random_number)
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'./document_{current_date}.txt'
    # with open(filename, 'w+') as file:
    #     file.write(datetime.now().strftime('%Y-%m-%d'))
    while num * 8 >= i >= (num - 1) * 8:
        i = i + 1
        headers = {
            'X-Forwarded-For': f'{random.randint(10, 126)}.{random.randint(10, 254)}.{random.randint(10, 254)}.{random.randint(10, 254)}'
        }
        url = (f'https://api-ddc-wscn.awtmt.com/market/rank?market_type=mdc&stk_type=stock&order_by=none&sort_field'
               f'=px_change_rate&limit=15&fields=prod_name%2Cprod_en_name%2Cprod_code%2Csymbol%2Clast_px%2Cpx_change'
               f'%2Cpx_change_rate%2Chigh_px%2Clow_px%2Cweek_52_high%2Cweek_52_low%2Cprice_precision%2Cupdate_time'
               f'&cursor={i}')
        res = httpx.get(url, headers=headers,verify=False).json()
        datalist = res['data']['candle']
        for item in datalist:
            if item[10] == item[8]:
                filter = {"property": "Name", "rich_text": {"contains": f'{item[0]}'}}
                query_result = notion.databases.query(database_id=database_id, filter=filter).get("results")
                length = len(query_result)
                if length == 0:
                    new_page = {
                        "Name": {"title": [{"text": {"content": f'{item[0]}'}}]},
                        "Code": {"rich_text": [{"type": "text", "text": {"content": f'{item[1]}'}}]},
                        "Tags": {"type": "multi_select", "multi_select": [{"name": f'{i}'}]},
                        "Date": {'type': 'date', 'date': {'start': str(current_date), 'end': None}},
                        "Number": {"number": 0},
                        "FilesCover": {"files": [{"type": "external", "name": "Cover",
                                                  "external": {
                                                      "url": "https://gw.alipayobjects.com/zos/bmw-prod/1c363c0b-17c6-4b00-881a-bc774df1ebeb.svg"}}]}
                    }
                    notion.pages.create(parent=parent, properties=new_page)
                    # send_dingtalk(item[0])
                # else:
                #     print(f'{item[0]}_________#######################__________')
                #     for result in query_result:
                #         page_id = result['id']
                #         number = result.get("properties").get("Number").get("number")
                #         new_page = {
                #             "Number": {"number": number},
                #             "Date": {'type': 'date', 'date': {'start': str(current_date), 'end': None}},
                #         }
                #         notion.pages.update(page_id=page_id, properties=new_page)
