# encoding=utf-8
from datetime import datetime
import httpx

if __name__ == '__main__':
    client = httpx.Client(timeout=10.0, headers=
    {
        "Notion-Version": "2022-06-28",
        "Authorization": "Bearer secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ",
        "Content-Type": "application/json"
    })
    database_id = '56641c6587cd400fb9037cf86a51d5d9'
    notion_token = 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ'
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'./document_{current_date}.txt'
    with open('./txt_dingfund.txt', 'r') as file:
        for item in file:
            data = {"parent": {
                "page_id": "5a055a5ef33c4a2eac7e6db00d3ce64c"
            }, "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "A note from your pals at Notion"
                            }
                        }
                    ]
                }
            }, "children": []}

        block_1= {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "You made this page using the Notion API. Pretty cool, huh? We hope you enjoy building with us."
                        }
                    }
                ]
            }
        };
        data["children"].append(block_1)
        response = client.post("https://api.notion.com/v1/pages", json=data)
