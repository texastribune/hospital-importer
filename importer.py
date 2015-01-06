import csv
import json
import os
import sys
from inflection import *
from helpers import *


class GeneralInformation(object):
    provider_numbers = []

    def __init__(self, filepath):
        self.filepath = filepath
        self.populate()

    def hospital(self, provider_number):
        with open(self.filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == provider_number:
                    return self.parse(row)

    def parse(self, row):
        return {
            "provider_number": clean(row[0]),
            "name": clean(row[1]),
            "address": clean(row[2]),
            "city": clean(row[5]),
            "zipcode": clean(row[7]),
            "county": clean(row[8]),
            "phone_number": format_phone(row[9]),
            "type": clean(row[10]),
            "hospital ownership": clean(row[11]),
            "emergency_services": clean(row[12]),
            "latitude": get_latitude(row[13]),
            "longitude": get_longitude(row[13]),
            "url": parameterize(unicode(row[1])),
        }

    def populate(self):
        with open(self.filepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.provider_numbers.append(row["Provider Number"])


def process(manifest, directory):
    hosp_file = os.path.join('./data', manifest["general-information"]["file"])

    index = 1
    general_info = GeneralInformation(hosp_file)

    for provider_number in general_info.provider_numbers:
        hospital = general_info.hospital(provider_number)
        hospital["_id"] = index
        index += 1
        print hospital


if __name__ == '__main__':
    try:
        print "Importing"
        with open('manifest.json') as jsonfile:
            manifest = json.loads(jsonfile.read())
        process(manifest, sys.argv[1])
    except IndexError, e:
        print "You will need to specify a target directory"
        sys.exit(1)


