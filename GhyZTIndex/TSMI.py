import math
from datetime import datetime, timedelta

from Common.dataProgress import get_position_range
from Common.readFile import read_csv_file
inputPath = "Data/"

def tsmi(input_data, t):
    tsmi_index = {}
    tsmi_index_page = {}

    # 遍历数据集
    for data_point in input_data:

        timestamp = datetime.strptime(data_point[0], "%Y-%m-%d %H:%M:%S")
        date_key = timestamp.date()

        # 使用timedelta计算时间对象对应的总秒数
        total_seconds = timedelta(hours=timestamp.hour, minutes=timestamp.minute, seconds=timestamp.second).total_seconds()
        time_key = int( total_seconds/t)

        # 如果日期键不存在，则创建一个新的日期键
        if date_key not in tsmi_index:
            tsmi_index[date_key] = {}

        # 如果时间键不存在，则创建一个新的时间键
        if time_key not in tsmi_index[date_key]:
            tsmi_index[date_key][time_key] = []

        # 将数据点添加到相应的时间键下
        tsmi_index[date_key][time_key].append(data_point)

    # #索引块的建立
    # for date_key in tsmi_index:
    #     tsmi_index_page[date_key] = {}
    #     for time_key in tsmi_index[date_key]:
    #         #不存在索引块创建新的索引块
    #         if int(time_key/340) not in tsmi_index_page[date_key]:
    #             tsmi_index_page[date_key][int(time_key/340)] = []
    #
    #         #添加数据块
    #         tsmi_index_page[date_key][int(time_key/340)].append(time_key)
        # 索引块的建立
    for date_key in tsmi_index:
        tsmi_index_page[date_key] = {}
        for time_key in tsmi_index[date_key]:

            # 不存在索引块创建新的索引块
            if int(time_key / 340) not in tsmi_index_page[date_key]:
                tsmi_index_page[date_key][int(time_key / 340)] = {}
                tsmi_index_page[date_key][int(time_key/340)][time_key] = []
                tsmi_index_page[date_key][int(time_key/340)]['range'] = [float('inf'), float(0), float('inf'), float(0)]

            #获取数据范围
            data_block = tsmi_index[date_key][time_key]
            range = get_position_range(data_block)
            row = [range[0], range[1], range[2], range[3]]

            # 添加数据块
            tsmi_index_page[date_key][int(time_key / 340)][time_key]= row

            index_range = tsmi_index_page[date_key][int(time_key/340)]['range']
            tsmi_index_page[date_key][int(time_key / 340)]['range'] = \
                [min(index_range[0], range[0]), max(index_range[1], range[1]), min(index_range[2], range[2]), max(index_range[3], range[3])]

    return tsmi_index, tsmi_index_page


if __name__ == '__main__':
    data_version = "Yneighbor"
    input_file = inputPath + data_version + '/(10, 7).csv'
    input_data = read_csv_file(input_file)
    tsmi(input_data,1)