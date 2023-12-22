# 遇事不要慌，先导个包吧
import pandas as pd
import numpy as np

# 造假数据
data = {'name':['严小样儿','严小样儿','严小样儿','才华横竖都溢','才华横竖都溢','才华横竖都溢','幽兰幽香','幽兰幽香','幽兰幽香'],
       'subject':['Python','C','SQL','Python','C','SQL','Python','C','SQL'],
       'score':[95,60,95,96,95,80,99,94,88]}

# 生成df
df = pd.DataFrame(data)
