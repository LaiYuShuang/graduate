from collections import OrderedDict

from Common.dataProgress import data_chansform
from Common.readFile import read_csv_file
from GhyZTIndex.TSMI import tsmi
from GhyZTIndex.ZASP import zasp

inputPath = "Data/"

def GhyZTIndex_construct(input_data):

    #空间划分映射
    zasp_index = OrderedDict(sorted(zasp(input_data, 3, 7).items(), key=lambda x: x[0]))

    GhyZTIndex = {}
    for index in zasp_index:
        GhyZTIndex[index] = {}
        data = zasp_index[index]
        zasp_data = data_chansform(data)
        for i in zasp_data:
            tsmi_index, tsmi_index_page = tsmi(input_data, 1)





if __name__ == '__main__':
    data_version = "Yneighbor"
    input_file = inputPath + data_version + '/(10, 7).csv'
    input_data = read_csv_file(input_file)
    GhyZTIndex_construct(input_data)