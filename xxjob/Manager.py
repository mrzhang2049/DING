import json
from easyNotion import easyNotion
import efinance as ef
import httpx
from datetime import datetime
import time
import pandas as pd
from pprint import pprint
from typing import List, Union
from easyNotion.blocksModel import Divider, Mention, LinkPreview, RichText, Block, TableX, ColumnList, Image
dbPage = easyNotion('d5c62b873aef4b77afc2e7870de97e38', 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ',
                    is_page=True)
current_date = datetime.now().strftime('%Y-%m-%d')
parent_id = dbPage.create_page(title=f"{current_date}周报", parent_id="d5c62b873aef4b77afc2e7870de97e38")
with open('./txt_dingfund.txt', 'r') as file:
    for item in file:
        baseinfo = ef.fund.get_base_info(item.strip())
        df1 = ef.fund.get_quote_history(baseinfo['基金代码'], 10)
        df1["单位净值"] = [str(ite) for ite in df1["单位净值"]]
        df1["Color"] = ["gray" if ite > 0 else 'red' for ite in df1["涨跌幅"]]
        df1["涨跌幅"] = [str(ite) for ite in df1["涨跌幅"]]
        json_data = json.loads(df1.to_json(orient='records'))
        for item in json_data:
            del item["累计净值"]
        json.dumps(json_data)








        content_blocks = [
            RichText(text_type="callout", id="", parent_id=parent_id, plain_text="callout",    annotations={"color": "red"}),
            ColumnList(parent_id=parent_id,
                       id='',
                       content=[
                           TableX("", json_data[:10], parent_id),
                           Image(parent_id,
                                 "https://gw.alipayobjects.com/zos/bmw-prod/b874caa9-4458-412a-9ac6-a61486180a62.svg"),
                       ]),
            # RichText(text_type="paragraph", id="", parent_id=parent_id, plain_text="paragraph" ),
            # RichText(text_type="quote", id="", parent_id=parent_id, plain_text="quote#@@@@@@@"),
        ]
        dbPage.insert_page(content_blocks)

# # 更新指定的行
# res = db.update({'Name': 'new_value'}, {'Name': '张三'})
# pprint(res)
# https://www.notion.so/FIND-5a055a5ef33c4a2eac7e6db00d3ce64c?pvs=4
# # 删除指定的行
# res = db.delete({'Name': 'new_value'})
# # pprint(res)
