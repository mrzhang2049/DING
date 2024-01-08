# easyNotion‼️使用限制
# 只可用于notion中数据库类型为"Database - Full page"的数据库
# 数据库中除title列其余所有列属性只能为text、ID、url
# 对页面的操作的支持度较低
# 易上手的代价是没有复杂的机制，未在大型项目上测试

from easyNotion import easyNotion
from pprint import pprint
from typing import List, Union
from easyNotion.blocksModel import Divider, Mention, LinkPreview, RichText, Block, TableX, ColumnList, Image

db = easyNotion('c4db279645344510acb15d556caffce1', 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ')
dbPage = easyNotion('adca7e5f3cc44781b42d972303d8bf35', 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ',
                    is_page=True)

# 获取全部数据表
# table = db.get_table()
# col = db.get_table()
# for itm in col:
#     print(itm.__getitem__('Name'))
# 查询指定的列
# col = db.query(['Filesmedia'], {'Name': '张三'})

# 插入新行
# res = db.insert(
#     {
#         "Name": '新年贺词里的人民情怀',
#         "Code": "12003",
#         "CheckValue": True,
#         "DAY": 'https://img2023.cnblogs.com/blog/35695/202312/35695-20231227181423297-1004649884.jpg',
#         "WEEK": 'https://img2023.cnblogs.com/blog/35695/202311/35695-20231121143812081-926795020.png',
#         "MONTH": 'https://gw.alipayobjects.com/zos/antfincdn/FLrTNDvlna/antv.png',
#
#     })

jsondata = [{
    "Name": 'cells',
    "Code": "cells",
    "Color": "red"
}, {
    "Name": 'cells',
    "Code": "cells",
    "Color": "green"
}]
content_blocks = [
    TableX(jsondata=jsondata, text_type="table", id="", parent_id="adca7e5f3cc44781b42d972303d8bf35"),
    TableX(jsondata=jsondata, text_type="table", id="", parent_id="adca7e5f3cc44781b42d972303d8bf35"),
    ColumnList(parent_id="adca7e5f3cc44781b42d972303d8bf35", text_type="column_list",
               id='',
               content=[
                   TableX(jsondata=jsondata, text_type="table", id="", parent_id="adca7e5f3cc44781b42d972303d8bf35")
                   , TableX(jsondata=jsondata, text_type="table", id="", parent_id="adca7e5f3cc44781b42d972303d8bf35")
               ]),
    ColumnList(parent_id="adca7e5f3cc44781b42d972303d8bf35", text_type="column_list",
               id='',
               content=[
                   Image(url="https://gw.alipayobjects.com/zos/bmw-prod/b874caa9-4458-412a-9ac6-a61486180a62.svg",
                         parent_id="adca7e5f3cc44781b42d972303d8bf35")
                   , Image(url="https://gw.alipayobjects.com/zos/bmw-prod/b874caa9-4458-412a-9ac6-a61486180a62.svg",
                           parent_id="adca7e5f3cc44781b42d972303d8bf35")
               ])
]
dbPage.insert_page(content_blocks)

# 更新指定的行
res = db.update({'Name': 'new_value'}, {'Name': '张三'})
pprint(res)

# 删除指定的行
res = db.delete({'Name': 'new_value'})
# pprint(res)
