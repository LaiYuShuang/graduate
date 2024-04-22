
#64位编码格式的Z-Order
import csv
import time
from collections import defaultdict

from pandas import np

from Common.dataProgress import get_position_range
from Common.readFile import read_csv_file

inputPath = "Data/"
class OpZorderMap:
    def __init__(self, min_x, max_x, min_y, max_y, num_levels):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.num_levels = num_levels
        self.level_width = (max_x - min_x) / (2 ** num_levels)
        self.level_height = (max_y - min_y) / (2 ** num_levels)

    # z-order编码
    def z_order(self,x,y):
        z = ''
        even = True
        x_range = [self.min_x,self.max_x]
        y_range = [self.min_y,self.max_y]
        while len(z) < 2 * self.num_levels:
            if even:
                mid = (x_range[0] + x_range[1]) / 2
                if x > mid:
                    bit = 1
                    x_range = (mid, x_range[1])
                else:
                    bit = 0
                    x_range = (x_range[0], mid)
            else:
                mid = (y_range[0] + y_range[1]) / 2
                if y > mid:
                    bit = 1
                    y_range = (mid, y_range[1])
                else:
                    bit = 0
                    y_range = (y_range[0], mid)
            z = z + str(bit)
            even = not even
        return z

    # 转化为规定的64位格式
    def z_order_fomat(self, z):
        length_encode = format(len(z),'08b')
        reserved_bit = '0' * (54 - len(z))
        encode = '00' + z + reserved_bit + length_encode
        return encode

    @classmethod
    def z_order_static(cls, x, y, min_x, max_x, min_y, max_y, num_levels):
        z = ''
        even = True
        x_range = [min_x, max_x]
        y_range = [min_y, max_y]
        while len(z) < 2 * num_levels:
            if even:
                mid = (x_range[0] + x_range[1]) / 2
                if x > mid:
                    bit = 1
                    x_range = (mid, x_range[1])
                else:
                    bit = 0
                    x_range = (x_range[0], mid)
            else:
                mid = (y_range[0] + y_range[1]) / 2
                if y > mid:
                    bit = 1
                    y_range = (mid, y_range[1])
                else:
                    bit = 0
                    y_range = (y_range[0], mid)
            z = z + str(bit)
            even = not even
        length_encode = format(len(z), '08b')
        reserved_bit = '0' * (54 - len(z))
        encode = '00' + z + reserved_bit + length_encode
        return encode


def op_z_order_index(input_data, num_levels):

    # 获取空间范围大小
    postion_range = get_position_range(input_data)

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
        z_code = int(zorder_map.z_order_fomat(zorder_map.z_order(x_position, y_position)),2)

        # 将当前行数据添加到对应的网格索引中
        z_index[z_code].append(row)
    return z_index, postion_range

def zasp(input_data, start_level, max_level):

    #计算网格内数据点数量标准值
    avg_points = len(input_data) // (2 ** start_level * 2 ** start_level)

    #初始Z-Order网格索引字典
    grid_index, position_range = op_z_order_index(input_data, start_level)

    #递归细分网格直到满足条件或者达到最大分解层次
    for level in range(start_level + 1, max_level + 1):
        # 标记超过标准值的网格
        exceeds_threshold = [z_order for z_order, indices in grid_index.items() if len(indices) > avg_points]

        #不存在超过标准值的网格
        if len(exceeds_threshold) == 0:
            break

        for z_order in exceeds_threshold:
            indices = grid_index[z_order]
            # new_range = get_position_range(indices)
            for data in indices:
                x = data[2]
                y = data[3]
                #计算下一级别Z-Order
                new_z_order = OpZorderMap.z_order_static(x,y,position_range[0],position_range[1],
                                                         position_range[2],position_range[3],level)
                grid_index[int(new_z_order,2)].append(data)
            grid_index.pop(z_order)
    return  grid_index

if __name__ == '__main__':
    data_version = "Yneighbor"
    input_file = inputPath + data_version + '/neighbors.csv'
    input_data = read_csv_file(input_file)

    instruct_time = []
    over_grird_count = []
    for start_level in range(2,13,2):
        timess = []
        count = []
        for max_level in range(2,12,2):

            #计算构建时间
            start_time = time.time()
            grid_index = zasp(input_data, start_level, max_level)
            end_time = time.time()
            execution_time = end_time - start_time
            timess.append(execution_time)

            # 计算结束时超过数目的
            num = 0
            for index in grid_index:
                data = grid_index[index]
                # print(index, len(data))
                if len(data) > (len(input_data) // (2 ** start_level * 2 ** start_level)):
                    num = num + 1
            count.append(num)

        instruct_time.append(timess)
        over_grird_count.append(count)

    for row in instruct_time:
        row_str = " ".join(str(time) for time in row)
        print(row_str)

    for row in over_grird_count:
        row_str = " ".join(str(count) for count in row)
        print(row_str)



    # # 指定CSV文件路径
    # csv_file = 'instruct_time.csv'
    # # 将二维数组写入CSV文件
    # with open(csv_file, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(instruct_time)
    #
    #     # 指定CSV文件路径
    #     csv_file = 'instruct_time.csv'
    # # 将二维数组写入CSV文件
    # with open(csv_file, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(instruct_time)