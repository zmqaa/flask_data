import plotly.express as px
import json
import plotly
def plot_data(data, x_column, y_column, chart_type='line', color_column=None, size_column=None):
    if x_column not in data.columns or y_column not in data.columns:
        raise ValueError(f"不存在的列: {x_column}, {y_column}. 可选择的列: {list(data.columns)}")

    # 创建图表
    if chart_type == 'line':
        fig = px.line(data, x=x_column, y=y_column, color=color_column, title='线图')
    elif chart_type == 'bar':
        fig = px.bar(data, x=x_column, y=y_column, color=color_column, title='柱状图')
    elif chart_type == 'scatter':
        fig = px.scatter(data, x=x_column, y=y_column, color=color_column, size=size_column, title='散点图')
    elif chart_type == 'pie':
        # 饼图需要提供 names 和 values
        fig = px.pie(data, names=x_column, values=y_column, title='饼图')
    elif chart_type == 'histogram':
        fig = px.histogram(data, x=x_column, title='直方图')
    elif chart_type == 'box':
        fig = px.box(data, x=x_column, y=y_column, title='箱线图')
    elif chart_type == 'heatmap':
        fig = px.density_heatmap(data, x=x_column, y=y_column, title='热图')
    else:
        raise ValueError(f"不支持的图: {chart_type}")

    # 自定义图表的布局
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        legend_title=color_column if color_column else None,
        title_font=dict(size=20),
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    fig_json = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    fig.show()
    return fig, fig_json

