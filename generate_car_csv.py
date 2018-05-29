import os
import csv
import io
from collections import defaultdict

def get_car_info(csvobject):
    """
    Generate dictionary with 'make' as key
    :param csvobject: csv.DictReader object
    :return car_info: defaultdict object
    """

    car_info = defaultdict(list)
    for row in csvobject:
        car_info[row['make']].append(row)
    return car_info

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=argparse.FileType('r', encoding='utf8'), default=None, help="In file in CSV format" )
    args = parser.parse_args()

    if not args.file:
        with open("C:\\disk\\ecuboost.eu\\auto_databases_one_March_2018_en.csv", encoding="utf8", newline="") as fh:
            fhcars = fh.read()

    reader = csv.DictReader(io.StringIO(fhcars), delimiter=',', dialect='excel')

    print(get_car_info(reader)['Talbot'])