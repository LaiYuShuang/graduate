import math
from collections import defaultdict

from Common.dataProgress import get_postion_range
from Common.readFile import read_csv_file
from GhyZTIndex.ZASP import OpZorderMap


def z_order_index(input_data, num_levels):

    # 获取空间范围大小
    postion_range = get_postion_range(input_data)

    min_x = postion_range[0]
    max_x = postion_range[1]
    min_y = postion_range[2]
    max_y = postion_range[3]

    #确定Z-order曲线参数
    zorder_map = OpZorderMap(min_x, max_x, min_y, max_y, num_levels)

    # 定义Z映射索引字典
    z_index = defaultdict(list)
    for i,row in enumerate(input_data):
        x_position = float(row[2])
        y_position = float(row[3])
        # 计算Z-Order索引64位bit 转换为了整形
        z_code = int(zorder_map.z_order(x_position, y_position),2)

        # 将当前行数据添加到对应的网格索引中
        z_index[z_code].append(i)
    return z_index, postion_range


def calculate_point_number(z_index, num_levels):
    list = [0]*((2**num_levels)*(2**num_levels)) #存放每个索引项下的点数量
    for index in z_index:
        target_data = []
        target_data.extend(z_index[index])
        list[index] = len(target_data)
    # 变为二维方阵
    n = len(list)
    side_length = int(math.sqrt(n))
    reshaped_array = [list[i:i + side_length] for i in range(0, n, side_length)]
    return reshaped_array

if __name__ == '__main__':
    input_file = 'Data/Yneighbor/neighbors.csv'
    input_data = read_csv_file(input_file)
    z_index,_ = z_order_index(input_data, 3)
    arr = calculate_point_number(z_index, 3)
    # 打印矩阵
    max_lengths = [max(len(str(elem)) for elem in row) for row in arr]
    for row in arr:
        aligned_row = [str(elem).ljust(max_lengths[i], ' ') for i, elem in enumerate(row)]
        print('\t'.join(aligned_row))


