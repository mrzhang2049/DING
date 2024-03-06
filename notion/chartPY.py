import numpy as np
import pandas as pd
# 创建子图使用make_subplots
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly as py

# x = np.linspace(0, 2, 100)
# y0 = np.random.randn(100) + 5
# y1 = np.random.randn(100)+ 15
#
# trace0 = go.Scatter(
#     x=x,
#     y=y0,
#     name="one"
# )
# trace1 = go.Scatter(
#     x=x,
#     y=y1,
#     name="two"
# )
# fig = go.Figure(
#     data=[trace0, trace1],
#     layout={"font": {"color": "cyan",
#                      "size": 20,
#                      "family": "stcaiyun"},
#             "template": "plotly_dark"
#             })
#


# trace0 = go.Bar(
#     # 方向变了，所以 x 轴和 y 轴的数据也要调换位置
#     y=["古明地觉", "芙兰朵露", "古明地恋"],
#     x=[87, 97, 85],
#     marker={
#         "color": "pink",
#         "opacity": 0.5,
#         "line": {
#             "width": 3,
#             "color": "cyan",
#         }
#     },
#     # 指定为水平方向即可
#     orientation="h"
# )
# fig = go.Figure(data=[trace0],
#                 layout={"template": "plotly_dark"})


# x0 = np.random.randn(1000)
# x1 = np.random.randn(1000)
# x2 = np.random.randn(500)
# trace0 = go.Histogram(
#     x=x0,
#     histnorm="probability",
#     marker={
#         "opacity": 0.75
#     }
# )
# trace1 = go.Histogram(
#     x=x1,
#     histnorm="probability",
#     marker={
#         "opacity": 0.75
#     }
# )
# trace3 = go.Histogram(
#     x=x2,
#     histnorm="probability",
#     marker={
#         "opacity": 0.75
#     }
# )
# fig = go.Figure(data=[trace0, trace1, trace3],
#                 layout={"title": "堆叠直方图",
#                         "template": "plotly_dark",
#                         "barmode": "stack"})
#
#
#
#
#
#
# x0 = np.random.randn(1000)
# x1 = np.random.chisquare(5, 1000)
# trace0 = go.Histogram(
#     x=x0,
#     histnorm="probability",
#     marker={
#         "opacity": 0.75
#     }
# )
# trace1 = go.Histogram(
#     x=x1,
#     histnorm="probability",
#     marker={
#         "opacity": 0.75
#     }
# )
# fig = go.Figure(data=[trace0, trace1],
#                 layout=dict(title="直方图", template="plotly_dark",
#                             xaxis={"dtick": 2, "range": [1, 20]}))


trace0 = go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5])
trace1 = go.Scatter(x=[2, 3, 4, 5, 6], y=[2, 3, 4, 5, 6])
trace2 = go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5])
trace3 = go.Scatter(x=[2, 3, 4, 5, 6], y=[2, 3, 4, 5, 6])

fig = make_subplots(rows=2,  # 将画布分为两行
                    cols=2,  # 将画布分为两列
                    subplot_titles=["trace0的标题",
                                    "trace1的标题",
                                    "trace3的标题",
                                    "trace4的标题"],  # 子图的标题
                    x_title="x轴标题",
                    y_title="y轴标题"
                    )
# 添加轨迹
fig.append_trace(trace0, 1, 1)  # 将trace0添加到第一行第一列的位置
fig.append_trace(trace1, 1, 2)  # 将trace1添加到第一行第二列的位置
fig.append_trace(trace2, 2, 1)  # 将trace2添加到第二行第一列的位置
fig.append_trace(trace3, 2, 2)  # 将trace3添加到第二行第二列的位置
fig.update_layout(height=600,
                  width=600,
                  title_text="多子图位置自定义")

fig = make_subplots(rows=1, cols=2)  # 1行2列

# 添加两个数据轨迹，构成两个图形
fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[5, 10, 15]),
    row=1, col=1  # 第一行第一列
)

fig.add_trace(
    go.Scatter(x=[20, 30, 40], y=[60, 70, 80]),
    row=1, col=2  # 第一行第二列
)

# 设置图形的宽高和标题
fig.update_layout(height=600,
                  width=800,
                  title_text="子图制作")

fig = make_subplots(rows=3, cols=2,
                    start_cell="bottom-left",  # 'bottom-left', 'top-left
                    # subplot_titles=["子图1", "子图2", "子图3", "子图4"]  # 每个子图的名字
                    )

# 添加4个数据轨迹
fig.add_trace(
    go.Bar(x=['2024-1-22', '2024-1-21', '2024-1-20', '2024-1-19', '2024-1-17', '2024-1-16'],
           y=[15, 4, -12, -1, -12, -9]),
    row=1, col=1  # 1*1
)

fig.add_trace(
    go.Scatter(x=[20, 30, 40], y=[60, 70, 80]),
    row=1, col=2  # 1*2
)

fig.add_trace(
    go.Scatter(x=[50, 60, 70], y=[30, 100, 60]),
    row=2, col=1  # 2*1
)
# fig.add_trace(
#     go.Bar(x=[50, 60, 70], y=[110, 30, 70]),
#     row=2, col=2  # 2*2
# )

# fig.add_trace(go.Pie(values=[2, 3, 1]),
#               2, 2)

fig.update_layout(height=600, showlegend=False,
                  width=800, title_text="多行多列子图制作")

# 比如绘制大洋洲（有澳大利亚和新西兰）
df = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df, x="year", y="lifeExp",
              color='country',  # 按照国家区分
              )

# 比如绘制大洋洲（有澳大利亚和新西兰）
df = px.data.gapminder().query("continent=='Oceania'")
fig = px.area(df, x="year", y="pop",
              color='country')  # 按照国家区分



trace1 = go.Scatter(
    x=[1, 2, 3],
    y=[4, 5, 6]
)
trace2 = go.Scatter(
    x=[20, 30, 40],
    y=[50, 60, 70],
    xaxis='x2',
    yaxis='y2'
)
trace3 = go.Scatter(
    x=[300, 400, 500],
    y=[600, 700, 800],
    xaxis='x3',
    yaxis='y3'
)
trace4 = go.Scatter(
    x=[4000, 5000, 6000],
    y=[7000, 8000, 9000],
    xaxis='x4',
    yaxis='y4'
)
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis=dict(
        domain=[0, 0.45]
    ),
    yaxis=dict(
        domain=[0, 0.45]
    ),
    xaxis2=dict(
        domain=[0.55, 1]
    ),
    xaxis3=dict(
        domain=[0, 0.45],
        anchor='y3'
    ),
    xaxis4=dict(
        domain=[0.55, 1],
        anchor='y4'
    ),
    yaxis2=dict(
        domain=[0, 0.45],
        anchor='x2'
    ),
    yaxis3=dict(
        domain=[0.55, 1]
    ),
    yaxis4=dict(
        domain=[0.55, 1],
        anchor='x4'
    )
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='multiple-subplots')
