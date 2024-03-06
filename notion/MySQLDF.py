import pandas as pd
from sqlalchemy import create_engine
import efinance as ef
# 初始化数据库连接
# 按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名
#engine = create_engine('mysql+pymysql://root:123456@localhost:3306/Fundx')
engine = create_engine("sqlite:////E://docker//admindb.db")

# # 如果觉得上方代码不够优雅也可以按下面的格式填写
# # engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format('root', '12345678', 'localhost', '3306', 'testdb'))
# # MySQL导入DataFrame
# # 填写自己所需的SQL语句，可以是复杂的查询语句
# sql_query = 'select * from product;'
# # 使用pandas的read_sql_query函数执行SQL语句，并存入DataFrame
# df_read = pd.read_sql_query(sql_query, engine)
# print(df_read)
df = ef.fund.get_fund_codes('zq')
print(df)

# DataFrame写入MySQL
# 新建DataFrame
#df_write = pd.DataFrame({'id': [10, 27, 34, 46], 'name': ['张三', '李四', '王五', '赵六'], 'score': [80, 75, 56, 99]})
# 将df储存为MySQL中的表，不储存index列
df.to_sql(name='product', con=engine, if_exists='append', index=False)