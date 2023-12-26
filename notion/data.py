import os
import sys
from pprint import pprint
from notion_client import Client
# Initialize the client
database_id = '61b85174dbb64557ae4721104bc267ab'
notion_token='secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
notion = Client(auth=notion_token)
new_page = {
    "Name": {"title": [{"text": {"content": 'H_%t'}}]},
    "Tags": {"type": "multi_select", "multi_select": [{"name": "Q@wer"}]},
    "Cover": {"files": [{"type": "external", "name": "Cover",
                         "external": {"url": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"}}]}
}
parent = {"database_id": database_id, "type": "database_id"}
notion.pages.create(parent=parent, properties=new_page)
