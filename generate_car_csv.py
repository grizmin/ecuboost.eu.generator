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

def write_car_csv(carsdict):
    # for carmake in carsdict.keys():
    for carmake in ['Audi']:
        with open('{}.csv'.format(carmake), 'w', newline='') as csvfile:
            fieldnames = ['Model', 'Year', 'Generation', 'Engine', 'Engine Type', 'Car Body', 'Drive', 'Gearbox']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in carsdict[carmake]:
                print(row)
                writer.writerow({'Model': row['model'], 'Year': row['year'], 'Engine': row['trim'], 'Generation': row['generation'],
                                 'Engine Type': row['engine_type'], 'Car Body': row['body'], 'Drive': row['drive'],
                                 'Gearbox': row['gearbox']})

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--infile', type=argparse.FileType('r', encoding='utf8'), default=None, help="In file in CSV format" )
    args = parser.parse_args()

    if not args.infile:
        with open("auto_databases_one_March_2018_en.csv", encoding="utf8", newline="") as fh:
            cars = fh.read()
    else:
        cars = infile.read()

    reader = csv.DictReader(io.StringIO(cars), delimiter=',', dialect='excel')

    write_car_csv(get_car_info(reader))