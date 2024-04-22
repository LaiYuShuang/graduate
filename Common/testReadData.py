import datetime

from Common.dataProgress import get_postion_range
from Common.readFile import read_csv_file

if __name__ == '__main__':
    input_data = read_csv_file('Data/Yneighbor/(10, 7).csv')
    range = get_postion_range(input_data)