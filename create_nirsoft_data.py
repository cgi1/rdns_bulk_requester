"""
A small script to bulk query rdns
@author: Christoph Giese <cgi1>
"""

import os
import random
import socket
import sys, csv, operator
import logging
import datetime
import argparse

import validators


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

def read_arguments_from_cli():
    parser = argparse.ArgumentParser(description='Read 1..n files with ip addresses and do reverse dns lookups')
    parser.add_argument('-if', '--file-input', dest="file_input",
                        help='File to read (only line separated files are supported)',
                        required=False)
    parser.add_argument('-id', '--dir-input', dest="dir_input",
                        help='Directory to read (only csv files from nirsoft are supported. See download_nirsoft_lists.sh) (Default: input_data)',
                        required=False, default='input_data')

    parser.add_argument('-ns', '--net-start', dest="net_start",
                        help='Network to scan: Start (e.g. 82.132.128.0)',
                        required=False)
    parser.add_argument('-ne', '--net-end', dest="net_end",
                        help='Network to scan: Start (e.g. 82.132.255.255)',
                        required=False)

    args = vars(parser.parse_args())

    return args


def get_ips_in_range(start, end):
    # Thanks to https://stackoverflow.com/questions/819355/how-can-i-check-if-an-ip-is-in-a-network-in-python
    import socket, struct
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]

def rate_from_nl_separtaed_file(file):

    networks_to_rate = []

    with open(file) as fin:
        for line in fin:

            line = line.rstrip()

            if validators.ipv4(line):
                networks_to_rate.append(line)
            else:
                logging.error("Line (%s) is not a valid IP." %line)

    logging.debug("Start to query rdns for (%s) IPs" % len(networks_to_rate))

    for ip in networks_to_rate:
        do_query(ip=ip)




def rate_from_csv_files(dir):
    largest_networks = []

    for filename in os.listdir(os.getcwd() + dir + '/'):

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


def rate_list_of_networks(networks_to_rate, complete=False):
    for network_to_rate in networks_to_rate:
        ips_in_range = get_ips_in_range(start=network_to_rate['NET_START'], end=network_to_rate['NET_END'])
        if not complete:
            a_thousand_random_ips = random.sample(ips_in_range, 1000)
        else:
            a_thousand_random_ips = ips_in_range
        for random_ip in a_thousand_random_ips:
            do_query(ip=random_ip)


def do_query(ip):
    try:
        host_by_addr = socket.gethostbyaddr(ip)
        print(host_by_addr)
        logging.debug(host_by_addr)
    except socket.herror:
        print("Unknown host(%s)" % ip)


def main(args, logger):

    if 'net_start' in args and args['net_start'] is not None and 'net_end' in args and args['net_end'] is not None:

        networks_to_rate = []
        networks_to_rate.append(
            {'country': 'GB', 'NET_START': args['net_start'], 'NET_END': args['net_end'], 'TOTAL_IPS': float(12345), # ToDo: total IPs.. Not needed here.
             'OWNER': 'o2'})
        rate_list_of_networks(networks_to_rate=networks_to_rate, complete=True)

    elif 'file_input' in args and args['file_input'] is not None:
        rate_from_nl_separtaed_file(file=args['file_input'])

    elif 'dir_input' in args and args['dir_input'] is not None:
        rate_from_csv_files(dir=args['dir_input'])

if __name__ == '__main__':
    # Only
    logger = init_logging()
    args = read_arguments_from_cli()
    main(args=args, logger=logger)

