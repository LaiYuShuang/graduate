from Common.dataProgress import data_time_format
from Common.readFile import read_csv_file
from GhyZTIndex.ZASP import OpZorderMap
import pandas as pd
if __name__ == '__main__':
    map = OpZorderMap(0,100,0,100,3)
    print(map.z_order_fomat(map.z_order(40,40)))
    print(int(map.z_order_fomat(map.z_order(40,40)),2))

    dataset = [[1,2,3,[1,2,3]]]
    df = pd.DataFrame(dataset)
    print(df[0])

    input_data = read_csv_file('Data/Yneighbor/neighbors.csv')
    idata = data_time_format(input_data, 1)