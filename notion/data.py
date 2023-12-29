import os
import sys
from pprint import pprint
from notion_client import Client
from datetime import datetime

# Initialize the client
database_id = '262f994ceb16421995492a5891fe7277'
notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
notion = Client(auth=notion_token)
current_date = datetime.now().strftime('%Y-%m-%d')
# new_page = {
#     "Name": {"title": [{"text": {"content": '2023年最后一个工作日热'}}]},
#     "Tags": {"type": "multi_select", "multi_select": [{"name": "er"}]},
#     "Cover": {"files": [{"type": "external", "name": "Cover",
#                          "external": {"url": "https://img.alicdn.com/imgextra/i4/O1CN01c26iB51UyR3MKMFvk_!!6000000002586-2-tps-124-122.png"}}]}
# }

new_page = {
    "Name":  'Vue实现docx/xlsx/pdf等类型文件预览功能_Vue.js_脚本宝典',
    "Tags":  "er",
    "Cover":  "https://img.alicdn.com/imgextra/i4/O1CN01c26iB51UyR3MKMFvk_!!6000000002586-2-tps-124-122.png"
}





parent = {"database_id": database_id, "type": "database_id"}
filter = {"property": "Name", "rich_text": {"contains": "wer"}}
query_result = notion.databases.query(database_id=database_id, filter=filter).get("results")
no_of_results = len(query_result)
sorts = [
        {
            "property": "Sort",
            "direction": "descending",
        }
    ]
if no_of_results == 0:
    print(no_of_results)
    notion.pages.create(parent=parent, properties=new_page)
else:
    for result in query_result:
        page_id = result['id']
        print(page_id)
        print(result.get("properties").get("Number").get("number"))
        new_page = {
            "Name": {"title": [{"text": {"content": 'Hello'}}]},
        }
        notion.pages.update(page_id=page_id,properties=new_page)
