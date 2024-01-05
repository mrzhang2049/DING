




# easyNotion‼️使用限制
# 只可用于notion中数据库类型为"Database - Full page"的数据库
# 数据库中除title列其余所有列属性只能为text、ID、url
# 对页面的操作的支持度较低
# 易上手的代价是没有复杂的机制，未在大型项目上测试

from easyNotion import easyNotion
from pprint import pprint
db = easyNotion('c4db279645344510acb15d556caffce1', 'secret_j4748C1PwOII5JWcVb1Myn5Vqyw75cn6ggDtf2dBMYQ')

# 获取全部数据表
table = db.get_table()
col = db.query(['Name'])
col = db.get_table()
for itm in col:
  print(itm.__getitem__('Name'))
# 查询指定的列
col = db.query(['Name'], {'Name': '张三'})
pprint(col)

# 插入新行
res = db.insert({'Name': 'Qew','Filesmedia':'https://img.alicdn.com/tfs/TB13DzOjXP7gK0jSZFjXXc5aXXa-212-48.png'})
pprint(res)

# 更新指定的行
res = db.update({'Name': 'new_value'},{'Name': '张三'})
pprint(res)

# 删除指定的行
res = db.delete({'Name': 'new_value'})
# pprint(res)






