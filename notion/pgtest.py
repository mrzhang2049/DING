import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd

index = np.arange(4)
data1 = [1, 5, 6, 3]
data2 = [1, 2, 3, 5]
data3 = [4, 8, 9, 4]
a = 0.3
plt.title('multi bar chart')

plt.bar(index,  # 条形图所在下标
        data1, a, color='pink', label='a')
plt.bar(index + a,
        data2, a, color='c', label='b')
plt.bar(index + 2 * a,
        data3, a, color='orange', alpha=0.5, label='c')
plt.legend()

colors = ['pink', 'orange', 'c']
df = pd.DataFrame([[4, 8, -2], [1, -5, 3], [2, 5, 4]])
df.plot(kind='bar', color=colors)

x = np.arange(1, 100)
print(x)
# 设置画布
fig = plt.figure(figsize=(20, 8), dpi=80)
# 使用add_subplot方法向 fig新增子图
#           #解释参数#
# (2,2,1)表示将画布分为2行2列，1表示占用序号为1的画布位置
ax1 = fig.add_subplot(2, 2, 1)
plt.plot(x, x)
ax2 = fig.add_subplot(2, 2, 2)
plt.plot(x, x ** 2)
ax3 = fig.add_subplot(2, 2, 3)
plt.plot(x, np.log(x))
# plt.show()


# x = range(0, 121)
# y = [random.randint(10, 30) for i in x]
# # 设置坐标轴名称
# plt.xlabel("时间", rotation=45)
# plt.ylabel("次数")
# # 设置坐标轴结点
# plt.plot(x, y, color='blue', linewidth=2, alpha=0.7)
# plt.title("每分钟心脏跳动数", color='red')

plt.savefig('simple_chart.png', dpi=300, bbox_inches='tight')  # dpi用于设置分辨率，bbox_inches避免白色边框
# plt.show()


# df.plot(x='Month', y=['Tmax', 'Tmin'])
#
# plt.show()


x = np.linspace(0, 10, 100)
y = np.sin(x)
# 创建图形和坐标轴(plt.figure(figsize=(12, 4)),设置了图形的大小为宽度为12英寸，高度为4英寸)
fig, ax = plt.subplots(figsize=(12, 4))
# 绘制曲线，设置y轴标签和曲线颜色
ax.plot(x, y, label='sin(x)', color='red')
# 添加标题和标签
ax.set_title('Sine Wave')
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
# 添加图例
ax.legend()
# 保存图形
plt.savefig('line_plot.png')
# 显示图形
plt.show()
