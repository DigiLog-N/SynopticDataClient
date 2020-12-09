import requests
import json
from time import time
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from time import sleep


def haversine_distance_estimation(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth, specified in decimal degrees. Inexpensive
    distance approximation. Taken from:
    https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_data_from(url):
    if 'output=csv' in url:
        csv_output = True
    else:
        csv_output = False

    t = time()
    result = requests.get(url)
    t = time() - t

    if result.status_code == 200:
        if csv_output:
            return result.text, t
        else:
            return result.json(), t
    else:
        # TODO: replace w/a set of proper Errors as needed
        print(result.text)
        raise ValueError("An error occured: %s" % str(result.status_code))


def get_time_series_for_last_24_hours_in_csv(token, stid):
    url = 'https://api.synopticdata.com/v2/stations/timeseries?stid=%s&recent=1440&token=%s&output=csv' % (stid, token)

    return get_data_from(url)


def get_time_series_for_last_month_in_csv(token, stid):
    # this is the largest value that can be supplied to recent= parameter.
    url = 'https://api.synopticdata.com/v2/stations/timeseries?stid=%s&recent=43200&token=%s&output=csv' % (stid, token)

    return get_data_from(url)


def get_time_series_for_last_year_in_csv(token, stid):
    now = datetime.utcnow()
    # instead of going back exactly one year from now, move back to the very beginning of that day.
    start_time = "%d%02d%02d%02d%02d" % (now.year - 1, now.month, now.day, now.hour, now.minute)
    end_time = "%d%02d%02d%02d%02d" % (now.year, now.month, now.day, now.hour, now.minute)

    url = 'https://api.synopticdata.com/v2/stations/timeseries?stid=%s&token=%s&output=csv&start=%s&end=%s' % (stid, token, start_time, end_time)

    return get_data_from(url)


def get_time_series_for_last_year_by_state(token, list_of_state_abbreviations):
    '''
    This query is to expensive to be allowed by Synoptic as is.
    :param token:
    :param list_of_state_abbreviations:
    :return:
    '''
    states_string = ','.join(list_of_state_abbreviations)

    now = datetime.utcnow()
    # instead of going back exactly one year from now, move back to the very beginning of that day.
    start_time = "%d%02d%02d0000" % (now.year, now.month, now.day-1)
    end_time = "%d%02d%02d0000" % (now.year, now.month, now.day)

    url = 'https://api.synopticdata.com/v2/stations/timeseries?token=%s&state=%s&start=%s&end=%s' % (token, states_string, start_time, end_time)

    return get_data_from(url)


def get_latest_data_by_state(token, list_of_state_abbreviations):
    # uses the 'latest' endpoint to get the latest data for each field from each station.
    # (there may be a threshold where inactive sensors aren't included).
    states_string = ','.join(list_of_state_abbreviations)

    url = 'https://api.synopticdata.com/v2/stations/latest?token=%s&state=%s' % (token, states_string)

    return get_data_from(url)


def extract_stations_from_latest_data():
    file = './data/latest/latest_data_for_ca_and_nh_at_1600401908.261241.json'

    with open(file, 'r') as f:
        with open('stations.txt', 'w') as of:
            j = json.load(f)
            for item in j['STATION']:
                lat = float(item['LATITUDE'])
                lon = float(item['LONGITUDE'])
                mnet_id = item['MNET_ID']
                stid = item['STID']
                name = item['NAME']
                state = item['STATE']

                distance = haversine_distance_estimation(lat, lon, 32.88, -117.23)

                of.write("%d\t%s\t%s\t%s\t%s\n" % (distance, state, mnet_id, stid, name))


def main(token, select_station_list):
    for station in select_station_list:
        results, elapsed_time = get_time_series_for_last_year_in_csv(token, station)
        filepath = 'data/yearly/%s.csv' % station
        with open(filepath, 'w') as f:
            f.write(str(results))
        sleep(5)


if __name__ == '__main__':
    '''
    2930P   La Jolla Shores
    DMHSD   Del Mar Heights
    MSDSD   Mt. Soledad
    4160P   University Heights
    CI150   Miramar
    F1955   FW1955 San Diego Midway
    NMLC1   SAN MARCOS SAN DIEGO
    BVDC1   MISSION VALLEY
    KEAC1   KEARNY MESA
    KCRQ    Carlsbad, McClellan-Palomar Airport
    1386P   NBC7 (Scripps Ranch)
    3025P   SDCCU Stadium
    PLMC1   PALOMAR AIRPORT
    CBDSD   Carlsbad
    KSAN    San Diego International Airport
    '''
    token = ''
    select_station_list = ['2930P','DMHSD','MSDSD','4160P','CI150','F1955','NMLC1','BVDC1','KEAC1','KCRQ','1386P','3025P','PLMC1','CBDSD']

    # wait one hour
    wait_time = 60 * 60

    while True:
        main(token, select_station_list)
        sleep(wait_time)

