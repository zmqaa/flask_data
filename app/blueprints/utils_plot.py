import plotly.express as px
import json
import plotly
import plotly.graph_objects as go
import numpy as np
def plot_data(data, x_column, y_columns, chart_type='line', color_column=None, size_column=None,
              use_moving_average=False, moving_average_window=5):
    # 确保 x 和 y 列在数据中
    if x_column not in data.columns or any(y not in data.columns for y in y_columns):
        raise ValueError(f"不存在的列: {x_column}, {y_columns}. 可选择的列: {list(data.columns)}")
    # 是否启用移动平均
    if use_moving_average:
        data = data.copy()  # 防止修改原数据
        for y_column in y_columns:
            data[y_column] = data[y_column].rolling(window=moving_average_window).mean()    # 更平滑的y轴
    # 创建图表
    if chart_type == 'line':
        # 按x轴的顺序来（对时间序列好用）
        data = data.sort_values(by=x_column)
        # 对于折线图，绘制每个 y_column 的线
        fig = go.Figure()
        for y_column in y_columns:
            fig.add_trace(go.Scatter(x=data[x_column], y=data[y_column], mode='lines', name=y_column))
        fig.update_layout(title='折线图', xaxis_title=x_column, yaxis_title='值')

    elif chart_type == 'bar':
        fig = px.bar(data, x=x_column, y=y_columns, color=color_column, title='柱状图')

    elif chart_type == 'scatter':
        fig = go.Figure()
        for y_column in y_columns:
            if size_column and size_column in data.columns:
                size_values = np.interp(data[size_column], (data[size_column].min(), data[size_column].max()),(10, 100))  # 归一化到 10-100 范围内
            else:
                size_values = 10
            fig.add_trace(go.Scatter(
                x=data[x_column],
                y=data[y_column],
                mode='markers',
                name=y_column,
                marker=dict(size=size_values)  # 这里是根据size_column调整大小
            ))

        fig.update_layout(title='散点图', xaxis_title=x_column, yaxis_title='值')

    elif chart_type == 'pie':
        fig = px.pie(data, names=x_column, values=y_columns[0], title='饼图')

    elif chart_type == 'histogram':
        fig = px.histogram(data, x=x_column, title='直方图')

    elif chart_type == 'box':
        fig = px.box(data, x=x_column, y=y_columns, title='箱线图')

    elif chart_type == 'heatmap':
        fig = px.density_heatmap(data, x=x_column, y=y_columns[0], title='热图')

    elif chart_type == 'area':
        fig = px.area(data, x=x_column, y=y_columns, color=color_column, title='面积图')

    elif chart_type == 'density':
        fig = px.density_contour(data, x=x_column, y=y_columns[0], title='密度图')

    elif chart_type == 'radar':
        fig = px.line_polar(data, r=y_columns[0], theta=x_column, line_close=True, title='雷达图')

    elif chart_type == 'bubble':
        if size_column and size_column in data.columns:
            size_values = np.interp(data[size_column], (data[size_column].min(), data[size_column].max()),
                                    (10, 100))  # 归一化到 10-100 范围内
        else:
            size_values = 10
        fig = px.scatter(data, x=x_column, y=y_columns[0], color=color_column, size=size_values, title='气泡图')

    elif chart_type == 'treemap':
        fig = px.treemap(data, path=[x_column], values=y_columns[0], title='树图')

    else:
        raise ValueError(f"不支持的图: {chart_type}")

    # 自定义图表的布局
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_columns[0],
        legend_title=color_column if color_column else None,
        title_font=dict(size=20),
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    fig_json = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    return fig, fig_json

