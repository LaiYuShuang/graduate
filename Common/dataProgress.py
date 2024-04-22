from pandas import np
import datetime

#统计地理空间最大最小值
def get_position_range(input_data):
    data = np.array(input_data)  # 转换为NumPy数组
    x = []
    y = []
    for row in data:
        x.append(float(row[2]))
        y.append(float(row[3]))
    min_x = np.min(x)
    max_x = np.max(x)
    min_y = np.min(y)
    max_y = np.max(y)
    postion_range = [min_x, max_x, min_y, max_y]
    return postion_range


#根据数据下标转化对应数据集
def data_chansform(input_data, index):
    data = []
    for i in index:
        data.append(input_data[i])
    return data
# #统计给定行的地理空间最大最小值
# def get_position_range(input_data, index):
#     data = []
#     for i in index:
#         data[i] = input_data[i]
#
#     data = np.array(data)  # 转换为NumPy数组
#     x = []
#     y = []
#     for row in data:
#         x.append(float(row[2]))
#         y.append(float(row[3]))
#     min_x = np.min(x)
#     max_x = np.max(x)
#     min_y = np.min(y)
#     max_y = np.max(y)
#     postion_range = [min_x, max_x, min_y, max_y]
#     return postion_range