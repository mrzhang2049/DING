import efinance as ef
import time
from notion_client import Client
from datetime import datetime
import random
from retrying import retry
# Initialize the client
database_id = '94d7835c3b6741c1a1ce0d9414b8bcbe'
notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
notion = Client(auth=notion_token)
current_date = datetime.now().strftime('%Y-%m-%d')
df = ef.fund.get_fund_codes('hh')
df.s
# with open(filename, 'w+') as file:
#     file.write(datetime.now().strftime('%Y-%m-%d'))

@retry(stop_max_attempt_number=3, wait_fixed=1000)
def some_unreliable_function(parent,properties):
    notion.pages.create(parent=parent, properties=properties)


for index, row in df.iterrows():
    name = df.iloc[index, 1]
    code = df.iloc[index, 0]
    new_page = {
        "Name": {"title": [{"type": "text", "text": {"content": name}}]},
        "Code": {"rich_text": [{"type": "text", "text": {"content": code}}]},
        "Cover": {"files": [{"type": "external", "name": "Cover",
                             "external": {
                                 "url": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"}}]}
    }
    random_number = random.random()
    print(index)
    parent = {"database_id": database_id, "type": "database_id"}
    some_unreliable_function(parent, new_page)

    # filter = {"property": "Name", "rich_text": {"contains": name}}
    # query_result = notion.databases.query(database_id=database_id, filter=filter).get("results")
    # no_of_results = len(query_result)
    # if no_of_results == 0:
    #     notion.pages.create(parent=parent, properties=new_page)
    # else:
    #     for result in query_result:
    #         page_id = result['id']
    #         print(page_id)
    #         print(result.get("properties").get("Number").get("number"))
    #         new_page = {
    #             "Name": {"title": [{"text": {"content": 'Hello'}}]},
    #         }
    #         notion.pages.update(page_id=page_id,properties=new_page)

print('_______________________________________________________________________________________________')
