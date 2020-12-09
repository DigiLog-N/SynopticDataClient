##############################################################################
# client.py
# Process a MesoWest/Synoptic-generated CSV file, and send it off though UDP,
# row by row.
# https://github.com/DigiLog-N/SynopticDataClient
# Copyright 2020 Canvass Labs, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
import socket
import sys
import json
import re
from time import sleep


host = '127.0.0.1'
port = 8888
sleep_between_packets = True
sleep_time = 0.25


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (host, port)


def read_csv_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
        d = {'header':{}}
        d['header']['stid'] = lines.pop(0).replace('# STATION: ', '').strip()
        d['header']['name'] = lines.pop(0).replace('# STATION NAME: ', '').strip()
        d['header']['lat'] = float(lines.pop(0).replace('# LATITUDE: ', '').strip())
        d['header']['lon'] = float(lines.pop(0).replace('# LONGITUDE: ', '').strip())
        d['header']['elev'] = float(lines.pop(0).replace('# ELEVATION [ft]: ', '').strip())
        d['header']['state'] = lines.pop(0).replace('# STATE: ', '').strip()
        d['header']['column_names'] = lines.pop(0).split(',')
        d['header']['column_units'] = lines.pop(0).split(',')

        # swap timestamp and station per John's request
        a = d['header']['column_names'][0]
        d['header']['column_names'][0] = d['header']['column_names'][1]
        d['header']['column_names'][1] = a

        lines = [x.split(',') for x in lines]

        d['lines'] = []

        for line in lines:
            a = line[0]
            line[0] = line[1]
            line[1] = a

            # sending it as a csv line means that it must stay string.
            #for i in range(0, len(line)):
            #    if re.match(r'^\d+$', line[i]) is not None:
            #        line[i] = int(line[i])
            #    elif re.match(r'^\d+\.\d+$', line[i]) is not None:
            #        line[i] = float(line[i])

            d['lines'].append(','.join(line))

        return d


def main():
    data = read_csv_file(sys.argv[1])

    print("Printing header in JSON format:\n")
    print(json.dumps(data['header'], indent=4))

    try:
        count = 0
        for line in data['lines']:
            sent = sock.sendto(line.encode(), server_address)
            count += 1
            if sleep_between_packets:
                sleep(sleep_time)
    finally:
        sock.close()
        print("\nSent %d rows." % count)


if __name__ == '__main__':
    main()
