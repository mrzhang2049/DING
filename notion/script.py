import os
import sys
from pprint import pprint
from notion_client import Client
# Initialize the client31
notion = Client(auth='secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ')
database_id= '61b85174dbb64557ae4721104bc267ab'
new_page = {
    "Name": {"title": [{"text": {"content": 'H_t'}}]},
    "Tags": {"type": "multi_select", "multi_select": [{"name": "Q@wer"}]}
}
parent = {"database_id": database_id, "type": "database_id"}
notion.pages.create(parent={"database_id": '61b85174dbb64557ae4721104bc267ab'}, properties=new_page)

print("You were added to the People database!")

# Query a database
name = input("\n\nEnter the name of the person to search in People: ")
results = notion.databases.query(
    **{
        "database_id": '61b85174dbb64557ae4721104bc267ab',
        "filter": {"property": "Name", "text": {"contains": name}},
    }
).get("results")

no_of_results = len(results)

if no_of_results == 0:
    print("No results found.")
    sys.exit()

print(f"No of results found: {len(results)}")

result = results[0]

print(f"The first result is a {result['object']} with id {result['id']}.")
print(f"This was created on {result['created_time']}")
