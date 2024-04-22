import csv
from datetime import datetime, timedelta
import pandas as pd

def read_csv_file(file):
    output_data = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # 跳过头部（列名）行
        for row in reader:
            row[1] = timedelta(seconds=float(row[1])) + datetime(2023, 3, 3, 0, 0, 0)
            data = [str(row[1]), float(row[5]), float(row[3]), float(row[4])]
            output_data.append(data)
    return output_data
