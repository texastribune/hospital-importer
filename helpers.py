import re


def yesNoToBool(cad):
    if cad.lower() == 'yes' or cad.lower() == 'true':
        return True
    else:
        return False

def get_latitude(cad):
    lat, lng = get_lat_long(cad)
    return lat

def get_longitude(cad):
    lat, lng = get_lat_long(cad)
    return lng

def get_lat_long(cad):
    return re.findall(r"[-+]?\d*\.\d+|\d+", cad)[-2:]

def clean(cad):
    try:
        return cad.strip()
    except AttributeError:
        return ""

def format_phone(cad):
    return "(%s) %s-%s" % tuple(cad.split('-'))

def parse_int(cad):
    try:
        return int(cad)
    except ValueError:
        return None

def parse_float(cad):
    try:
        return float(cad)
    except ValueError:
        return None
