import pygal

# 创建一个 Line 类型的图表
chart = pygal.Line()

# 添加数据到图表
chart.add('Series A', [1, 2, 3, 4, 5])
chart.add('Series B', [5, 4, 3, 2, 1])

# 设置图表标题等属性（如果需要）
chart.title = 'My Chart'
chart.x_labels = ['A', 'B', 'C', 'D', 'E']

# 将图表保存为 PNG 格式
chart.render_to_png('my_chart.png')

