import os
import csv
import io
from collections import defaultdict
import time


class CarGenerator:
    """
    Generates and writes car csv files from a given csv database.
    Note: The csv database must contain the following fields:
    trim,make,model,generation,body,drive,gearbox,engine_type,engine_volume,engine_power,year
    """

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

    def write_car_csv(self, carsdict, make=None, sort=None):
        """
        Writes Car CSV files to a given folder.

        :param carsdict: defaultdict object - output from get_car_info
        :param make: optional make parameter, sting, in case you want to generate only specific make
        :return:
        """
        # for carmake in carsdict.keys():
        makes = [make] if make else carsdict.keys()
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        for carmake in makes:
            with open(self.folder + os.sep + '{}.csv'.format(carmake), 'w', newline='') as csvfile:
                if not self.fieldnames:
                    self.fieldnames = ['Model', 'Year', 'Generation', 'Engine', 'Engine Type', 'Car Body',
                                       'Drive', 'Gearbox']
                car_selection = carsdict[carmake]
                if sort:
                    def sort_mixed_type_list_of_dict_items(seq):
                        # Collect the values by type
                        d = defaultdict(list)
                        for x in seq:
                            d['int' if x[sort].isdigit() else 'str'].append(x)
                        # Sort each type
                        d = {k: iter(sorted(v, key=lambda x: x[sort] if k == 'str' else int(x[sort]))) for k, v in d.items()}
                        # The result list - maintain the default str<>int order with iterator object
                        result = [next(d['int' if x['model'].isdigit() else 'str']) for x in seq]
                        # print([x[sort] for x in result])
                        return result

                    car_selection = sort_mixed_type_list_of_dict_items(car_selection)

                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
                for row in car_selection:
                    writer.writerow({'Model': row['model'], 'Year': row['year'], 'Engine': row['trim'], 'Generation':
                                    row['generation'], 'Engine Type': row['engine_type'], 'Car Body': row['body'],
                                    'Drive': row['drive'], 'Gearbox': row['gearbox']})
            print('{}.csv written.'.format(carmake))
        return

    def run(self, make=None, sort='model'):
        """
        Self explainatory

        :param make: Optional Make. Use it if you want to generate only 1 make instad of all.
        :param sort: sort key, must be one of the infile csv field names. Defaults to 'model'
        :return: time taken
        """
        start = time.time()
        self.write_car_csv(self.get_car_info(self.cars), make=make, sort=sort)
        stop = time.time()
        time_taken = stop - start
        return time_taken


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--infile', type=argparse.FileType('r', encoding='utf8'), default=None,
                        help="In file in CSV format")
    args = parser.parse_args()
    if not args.infile:
        gencars = CarGenerator('auto_databases_one_March_2018_en.csv')
    else:
        gencars = CarGenerator(args.infile)

    time_taken = gencars.run()

    print('[*] Time taken: {0:.2f} seconds.'.format(time_taken))