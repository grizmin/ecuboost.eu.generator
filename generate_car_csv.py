import os
import csv
import io
from collections import defaultdict
import time

class CarGenerator:

    def __init__(self, file, folder='cars', fieldnames=None):
        self.folder = folder
        self.fieldnames = fieldnames
        try:
            with open(file, encoding="utf8", newline="") as fh:
                scars = fh.read()
            self.cars = csv.DictReader(io.StringIO(scars), delimiter=',', dialect='excel')
        except Exception:
            print("Ops. There is something wrong accessing {}".format(file))
            raise

    def get_car_info(self, csvobject):
        """
        Generate dictionary with 'make' as key
        :param csvobject: csv.DictReader object
        :return car_info: defaultdict object
        """

        car_info = defaultdict(list)
        for row in csvobject:
            car_info[row['make']].append(row)
        return car_info

    def write_car_csv(self, carsdict, make=None):
        # for carmake in carsdict.keys():
        makes = [make] if make else carsdict.keys()
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        for carmake in makes:
            with open(self.folder + os.sep + '{}.csv'.format(carmake), 'w', newline='') as csvfile:
                if not self.fieldnames:
                    self.fieldnames = ['Model', 'Year', 'Generation', 'Engine', 'Engine Type', 'Car Body', 'Drive', 'Gearbox']
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)

                writer.writeheader()
                for row in carsdict[carmake]:
                    # print(row)
                    writer.writerow({'Model': row['model'], 'Year': row['year'], 'Engine': row['trim'], 'Generation': row['generation'],
                                     'Engine Type': row['engine_type'], 'Car Body': row['body'], 'Drive': row['drive'],
                                     'Gearbox': row['gearbox']})
            print('{}.csv written.'.format(carmake))

    def run(self, make=None):
        start = time.time()
        self.write_car_csv(self.get_car_info(self.cars),make=make)
        stop = time.time()
        time_taken = stop - start
        return time_taken

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--infile', type=argparse.FileType('r', encoding='utf8'), default=None, help="In file in CSV format" )
    args = parser.parse_args()

gencars = CarGenerator('auto_databases_one_March_2018_en.csv')
print('[*] Time taken: {0:.2f} seconds.'.format(gencars.run()))