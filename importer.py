import csv
import json
import os
import sys
from inflection import *
from helpers import *

class StateIndicators(object):
    def __init__(self, basepath, config):
        self.basepath = basepath
        self.config = config

    def to_dict(self):
        return self.import_emergency_care(self.config["emergency_care"])

    def import_emergency_care(self, filename):
        output = {}
        measures = ["ED_1b", "OP_18b", "OP_20"]
        columns = {
            "measure_id": 3,
            "value": 4
        }
        with open(os.path.join(self.basepath, filename)) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == "TX":
                    if row[columns["measure_id"]] in measures:
                        output[row[columns["measure_id"]].lower()] = parse_float(row[columns["value"]])
        return output


class NationalIndicators(object):
    def __init__(self, basepath, config):
        self.basepath = basepath
        self.config = config

    def to_dict(self):
        return dict(self.import_emergency_care(self.config["emergency_care"]), **self.import_readmission_rates(self.config["readmission_rates"]))

    def import_emergency_care(self, filename):
        output = {}
        measures = ["ED_1b", "OP_18b", "OP_20"]
        columns = {
            "measure_id": 1,
            "value": 4
        }
        with open(os.path.join(self.basepath, filename)) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[columns["measure_id"]] in measures:
                    output[row[columns["measure_id"]].lower()] = parse_float(row[columns["value"]])
        return output

    def import_readmission_rates(self, filename):
        output = {}
        measures = [
            "MORT_30_PN", "MORT_30_HF", "MORT_30_AMI", "READM_30_AMI",
            "MORT_30_HF", "READM_30_HOSP_WIDE", "READM_30_PN", "COMP_HIP_KNEE",
            "PSI_4_SURG_COMP", "PSI_90_SAFETY"
        ]
        columns = {
            "measure_id": 1,
            "value": 2
        }
        with open(os.path.join(self.basepath, filename)) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[columns["measure_id"]] in measures:
                    output[row[columns["measure_id"]].lower()] = parse_float(row[columns["value"]])
        output["serious_complications"] = output["psi_90_safety"]
        output["death_from_serious_complications"] = output["psi_4_surg_comp"]
        return output


class OutcomeIndicators(object):
    # Readmissions Complications and Deaths - Hospital.csv
    measures = {
        "Acute Myocardial Infarction (AMI) 30-Day Readmission Rate": "readm_30_ha",
        "Heart failure (HF) 30-Day Readmission Rate": "readm_30_hf",
        "Pneumonia (PN) 30-Day Readmission Rate": "readm_30_pn",
        "Rate of readmission after hip/knee surgery": "readm_30_hip_knee",
        "Rate of readmission after discharge from hospital (hospital-wide)": "readm_30_hosp_wide",

        "Acute Myocardial Infarction (AMI) 30-Day Mortality Rate": "mort_30_ami",
        "Heart failure (HF) 30-Day Mortality Rate": "mort_30_hf",
        "Pneumonia (PN) 30-Day Mortality Rate": "mort_30_pn",
        "Rate of complications for hip/knee replacement patients": "comp_hip_knee"
    }

    def __init__(self, filepath):
        self.filepath = filepath

    def provider(self, provider_number):
        output = {}
        with open(self.filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == provider_number:
                    if row[8] in self.measures:
                        output[self.measures[row[8]]] = parse_float(row[12])
        return output


class ComplicationIndicators(object):
    measures = {
        "Deaths among Patients with Serious Treatable Complications after Surgery": "death_from_serious_complications",
        "Serious complications": "serious_complications"
    }

    def __init__(self, filepath):
        self.filepath = filepath

    def provider(self, provider_number):
        output = {}
        with open(self.filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == provider_number:
                    if row[8] in self.measures:
                        output[self.measures[row[8]]] = row[10]
        return output


class AssociatedInfections(object):
    measures = {
        "Central line-associated blood stream infections (CLABSI)": "hai_1",
        "Catheter-Associated Urinary Tract Infections (CAUTI)": "hai_2",
        "Surgical Site Infection from colon surgery (SSI: Colon)": "hai_3",
        "Surgical Site Infection from abdominal hysterectomy (SSI: Hysterectomy)": "hai_4"
    }

    def __init__(self, filepath):
        self.filepath = filepath

    def provider(self, provider_number):
        output = {}
        with open(self.filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == provider_number:
                    if row[8] in self.measures:
                        key = self.measures[row[8]]
                        output[key] = parse_float(row[11])
                        output[key + "_desc"] = row[10]
        return output


class EmergencyRates(object):
    measures = ['ED_1b', 'OP_18b', 'OP_20']

    def __init__(self, filepath):
        self.filepath = filepath

    def provider(self, provider_number):
        output = {}
        with open(self.filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == provider_number:
                    for measure in self.measures:
                        if row[9] == measure:
                            output[measure.lower()] = parse_int(row[11])
        return output


class QualityIndicators(object):
    measures = [
        "H_QUIET_HSP_A_P",
        "H_QUIET_HSP_A_P",
        "H_HSP_RATING_9_10",
        "H_RECMND_DY",
        "H_COMP_2_A_P",
        "H_COMP_3_A_P",
        "H_COMP_1_A_P",
        "H_CLEAN_HSP_A_P"
    ]

    def __init__(self, filepath):
        self.filepath = filepath

    def provider(self, provider_number):
        output = {}
        with open(self.filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == provider_number:
                    for measure in self.measures:
                        if row[8] == measure:
                            output[measure.lower()] = parse_int(row[11])
        return output


class GeneralInformation(object):
    provider_numbers = []

    def __init__(self, filepath):
        self.filepath = filepath
        self.populate()

    def provider(self, provider_number):
        with open(self.filepath, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[2] == provider_number:
                    return self.parse(row)

    def parse(self, row):
        return {
            "provider_number": clean(row[2]),
            "name": clean(row[3]),
            "address": clean(row[4]),
            "city": clean(row[7]),
            "zipcode": clean(row[9]),
            "phone_number": format_phone(row[11]),
            "type": clean(row[12]),
            "hospital ownership": clean(row[13]),
            "emergency_services": clean(row[14]),
            "latitude": get_latitude(row[15]),
            "longitude": get_longitude(row[15]),
            "url": parameterize(unicode(row[3])),
        }

    def populate(self):
        with open(self.filepath, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[2] != "":
                    # Closed hospitals are omitted
                    self.provider_numbers.append(row[2])


class Processor(object):
    def __init__(self, manifest, directory):
        self.manifest = manifest
        self.directory = directory
        self.populate()

    def populate(self):
        hospital_data = json.loads('data/hospitals-2014.json')
        self.cache = {}
        for hospital in hospital_data:
            self.cache[hospital["provider_number"]] = hospital["url"]

    def provider(self, provider_number):
        hosp_file = os.path.join('./data', self.manifest["general_information"]["file"])
        emer_file = os.path.join(self.directory, self.manifest["emergency_care"]["file"])
        quality_file = os.path.join(self.directory, self.manifest["quality_indicators"]["file"])
        infec_file = os.path.join(self.directory, self.manifest["associated_infections"]["file"])
        comp_file = os.path.join(self.directory, self.manifest["complications_rates"]["file"])
        outcome_file = os.path.join(self.directory, self.manifest["outcomes"]["file"])

        output = GeneralInformation(hosp_file).provider(provider_number)
        output["emergency_care"] = EmergencyRates(emer_file).provider(provider_number)
        output["quality_indicators"] = QualityIndicators(quality_file).provider(provider_number)
        output["associated_infections"] = AssociatedInfections(infec_file).provider(provider_number)
        output["complications_rates"] = ComplicationIndicators(comp_file).provider(provider_number)
        output["outcomes"] = OutcomeIndicators(outcome_file).provider(provider_number)

        return output

    def state(self):
        return StateIndicators(self.directory, self.manifest["state"]).to_dict()

    def national(self):
        return NationalIndicators(self.directory, self.manifest["national"]).to_dict()

    def to_feature(self, hospital, index=1):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    hospital["latitude"],
                    hospital["longitude"]
                ]
            },
            "type": "Feature",
            "properties": {
                "description": "%s, %s - %s" % (hospital["address"], hospital["city"], hospital["zipcode"]),
                "id": index,
                "title": hospital["name"]
            }
        }

    def to_zipcode(self, hospital):
        return [hospital["zipcode"], [hospital["latitude"], hospital["longitude"]]]

    def store_hospital(self, hospital, index=1):
        with open("output/%s.json" % index, "w") as jsonfile:
            jsonfile.write(json.dumps(hospital))

    def to_json(self):
        hospitals = []
        zipcodes = {}
        geojson = {
        "type": "FeatureCollection",
        "bbox": [
            -106.49985294199968,
            25.91785218500047,
            -93.76764915199965,
            36.19071202900045
        ],
        "features": []}

        with open("output/state.json", "w") as jsonfile:
            jsonfile.write(json.dumps(self.state()))

        with open("output/national.json", "w") as jsonfile:
            jsonfile.write(json.dumps(self.national()))

        index = 1
        hosp_file = os.path.join('./data', self.manifest["general_information"]["file"])
        general_info = GeneralInformation(hosp_file)

        for provider_number in general_info.provider_numbers:
            hospital = self.provider(provider_number)
            hospital["_id"] = index
            geojson["features"].append(self.to_feature(hospital, index))
            zipcode, coords = self.to_zipcode(hospital)
            zipcodes[zipcode] = coords
            hospitals.append(hospital)

            self.store_hospital(hospital, index)
            index += 1

        with open("output/zipcodes.json" % index, "w") as jsonfile:
            jsonfile.write(json.dumps(zipcodes))

        with open("output/hospitals.geojson" % index, "w") as jsonfile:
            jsonfile.write(json.dumps(geojson))

        with open("output/hospitals.json" % index, "w") as jsonfile:
            jsonfile.write(json.dumps(hospitals))


if __name__ == '__main__':
    try:
        print "Importing"
        with open('manifest.json') as jsonfile:
            manifest = json.loads(jsonfile.read())
        processor = Processor(manifest, sys.argv[1])
        processor.to_json()

    except IndexError, e:
        print "You will need to specify a target directory"
        sys.exit(1)
