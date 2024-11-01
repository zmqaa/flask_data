import plotly.express as px

def plot_data(data, x_column, y_column, chart_type='line'):
    if x_column not in data.columns or y_column not in data.columns:
        raise ValueError(f"不存在的列: {x_column}, {y_column}. 可选择的列: {list(data.columns)}")

    if chart_type == 'line':
        fig = px.line(data, x=x_column, y=y_column)
    elif chart_type == 'bar':
        fig = px.bar(data, x=x_column, y=y_column)
    elif chart_type == 'scatter':
        fig = px.scatter(data, x=x_column, y=y_column)
    else:
        raise ValueError(f"不支持的图: {chart_type}")

    fig.show()


