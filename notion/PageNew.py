from notion.block import TextBlock,ImageBlock
from notion_client import Client

# 替换为你的Notion Integration Token
NOTION_API_KEY = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
# 初始化客户端
client = Client(auth=NOTION_API_KEY)
# 定义父页面ID
parent_page_id = ''
# 定义要创建的新页面标题
title = "New Page Title"


database_id = '3e2039f7d3b24715a573641732215d37'
notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
notion = Client(auth=notion_token)
notion.pages.create(
    parent={"page_id": parent_page_id},
    properties={
        "Title": {"title": [{"text": {"content": title}}]},
        "body": [
            TextBlock(text='Hello, this is a new page created using Python!'),
            ImageBlock(image='https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png')
        ]
    }
)
