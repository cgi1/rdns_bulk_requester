"""
A small script to bulk query
@author: Christoph Giese <cgi1>
"""

import os
import random
import socket
import sys, csv, operator
import logging
import datetime


def init_logging():
    logFormatter = logging.Formatter("[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s")
    rootLogger = logging.getLogger()
    LOG_DIR = os.getcwd() + '/' + 'logs'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    timestamp = datetime.datetime.now()
    fileHandler = logging.FileHandler("{0}/{1}_{2}.log".format(LOG_DIR, timestamp, "create_nirsoft_data"))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    rootLogger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger

def get_ips_in_range(start, end):
    # Thanks to https://stackoverflow.com/questions/819355/how-can-i-check-if-an-ip-is-in-a-network-in-python
    import socket, struct
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]


def rate_list_of_networks(networks_to_rate, complete=False):
    for network_to_rate in networks_to_rate:
        ips_in_range = get_ips_in_range(start=network_to_rate['NET_START'], end=network_to_rate['NET_END'])
        if not complete:
            a_thousand_random_ips = random.sample(ips_in_range, 1000)
        else:
            a_thousand_random_ips = ips_in_range
        for random_ip in a_thousand_random_ips:
            try:
                host_by_addr = socket.gethostbyaddr(random_ip)
                print(host_by_addr)
                logging.debug(host_by_addr)
            except socket.herror:
                print("Unknown host(%s)" % random_ip)

init_logging()

def rate_from_csv_files():
    largest_networks = []

    for filename in os.listdir(os.getcwd()):

        if not filename.startswith('networks_'):
            continue

        country = filename.split('networks_')[1].split('.')[0]

        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            sortedlist = sorted(reader, key=lambda row: (row['TOTAL_IPS']), reverse=False)
            added_networks_per_country = 0

            for item in sortedlist:
                if added_networks_per_country > 5:
                    break
                largest_networks.append({'country': country, 'NET_START': item['NET_START'], 'NET_END': item['NET_END'], 'TOTAL_IPS': float(item['TOTAL_IPS']), 'OWNER': item['OWNER']})
                added_networks_per_country += 1

    print("Created list of largest networks.. Start resolution")
    largest_networks = sorted(largest_networks, key=lambda k: k['TOTAL_IPS'], reverse=True)
    rate_list_of_networks(networks_to_rate=largest_networks)



#rate_from_csv_files()
networks_to_rate = []
networks_to_rate.append({'country': 'GB', 'NET_START': '82.132.128.0', 'NET_END': '82.132.255.255', 'TOTAL_IPS': float(32768), 'OWNER': 'o2'})
rate_list_of_networks(networks_to_rate, complete=True)