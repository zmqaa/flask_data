import pandas as pd


def fill_missing_values(data, method='ffill'):
    if method == 'ffill':
        data = data.fillna(method='ffill')
    elif method == 'bfill':
        data = data.fillna(method='bfill')
    elif method == 'mean':
        for col in data.select_dtypes(include=['float', 'int']).columns:
            data[col].fillna(data[col].mean(), inplace=True)
    elif method == 'median':
        for col in data.select_dtypes(include=['float', 'int']).columns:
            data[col].fillna(data[col].median(), inplace=True)

    return data


def remove_outliers(data, columns):
    for column in columns:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        data = data[(data[column] >= (q1 - 1.5 * iqr)) & (data[column] <= (q3 + 1.5 * iqr))]
    return data


def clean_data(data, unneccessary_columns=None, outlier_columns=None, fillna_method='ffill'):
    # 首先确保数据是DataFrame格式
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    elif not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    # 删除重复行
    data = data.drop_duplicates()

    # 填充缺失值
    data = fill_missing_values(data, method=fillna_method)

    # 转换数据类型（示例：将日期列转换为日期格式）
    if 'date_column' in data.columns:
        data['date_column'] = pd.to_datetime(data['date_column'], errors='coerce')

    # 去除不必要的列
    if unneccessary_columns:
        data = data.drop(columns=unneccessary_columns, errors='ignore')

    # 异常值处理
    if outlier_columns:
        data = remove_outliers(data, outlier_columns)

    return data

def get_original_metrics(data):
    metrics = {
        '大小': data.shape,    # 元组(行数，列数)
        '列名': data.columns.tolist(),    # 列名的列表
        '缺失值': data.isnull().sum().to_dict(),   # 字典 {'c1': 0, 'c2':1}...
        '列类型': data.dtypes.to_dict()   #字典 {'c1': int64, 'c2': float64}...
    }
    return metrics

def get_cleaned_metrics(data):
    metrics = {
        '大小': data.shape,
        '缺失值': data.isnull().sum().to_dict(),
        '类型': data.dtypes.to_dict()
    }
    return metrics

def get_descriptive_stats(data):
    stats = {
        "均值": data.mean(numeric_only=True),
        "标准差": data.std(numeric_only=True),
        "中位数": data.median(numeric_only=True),
        "最小值": data.min(numeric_only=True),
        "最大值": data.max(numeric_only=True),
        "偏度": data.skew(numeric_only=True),
        "峰度": data.kurtosis(numeric_only=True),
    }
    # 创建成dataframe,字典的key为行
    stats_df = pd.DataFrame(stats)
    # 计数
    stats_df = stats_df.style.format('{:.2f}')
    return stats_df

