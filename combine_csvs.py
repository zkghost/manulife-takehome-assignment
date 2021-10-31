"""
Utility that combines CSVs into a single file. 
Assumptions:
- CSV files are written under a specific folder (see FILE_LOCATION const var)
- CSV filenames end with .csv
- CSV filenames correspond to regions or environments
    - prior the .csv suffix, if the filename ends with a number, all files with
      the same prefix will share the same label, ie:
        Filename      Row
        NA Prod 1.csv 1.1.1.1, 0, 0 
        NA Prod 2.csv 2.2.2.2, 1, 2
        
        In this case, both rows will be associated with environment name NA Prod
- The first row of the CSV corresponds to an IPv4 address (ex: 192.168.100.1)

"""
from collections import defaultdict
import csv
from pathlib import Path
import re
import socket

# TODO: Dynamically get absolute path from run location...
#       or run in docker to not worry about it
FILE_LOCATION = "Engineering Test Files"
OUTPUT_FILE = 'Combined.csv'
OUTPUT_FIELDS = ['Source IP', 'Environment']

def get_csv_file_list(files):
    """
    Filters strings in files to those that end with .csv and 
    do not have the same name as OUTPUT_FILE

    Input:
        files: list of str filenames
    """
    return [x for x in files if x.endswith('.csv') and 
                                x != OUTPUT_FILE]

def parse_filename(filename):
    """
    Given a string filename, returns the string with:
        - trailing digits stripped
        - .csv suffix stripped
        - leading/trailing whitespace stripped

    Input:
        - filename: str
    """
    regex = '\d+'
    return  re.split(regex, filename)[0]\
              .replace('.csv', '')\
              .strip()

def get_region_ips(rows):
    """
    Given a set of rows, returns all IP addresses in file. 
    Expects rows to come from csv.reader where first row is 
    csv column headers. 

    Input: 
        - rows: iterable, rows from csv.reader object
    """
    first = False
    ips = []
    for row in rows:
        if not first:
            # skip the column headers
            first = True
            continue
        ips.append(row[0])
    return ips

def write_output_csv(ip_region_pairs):
    """
    Given a set of ip_region_pairs, sorts them in ascending order
    by IP address and writes them out to OUTPUT_FILE. Files
    will be written inside FILE_LOCATION directory. 
    
    Inputs:
        - ip_region_pairs: iterable consisting of tuples of (ip_address, environment name)
        - output: str, name of the output file
    """
    ip_region_pairs = list(ip_region_pairs)
    # use socket.inet_aton to sort ip addrs by value
    ip_region_pairs.sort(key=lambda x: socket.inet_aton(x[0]))
    with open(FILE_LOCATION + f'/{OUTPUT_FILE}', 'w+') as f:
        f.write(','.join(OUTPUT_FIELDS) +'\n')
        for pair in ip_region_pairs:
            f.write(','.join(pair) + '\n')


def main():
    # get all files in expected dir
    files = [f.name for f in Path(FILE_LOCATION).iterdir() if f.is_file()]
    # filter to set of files we want to process
    files = get_csv_file_list(files)

    # next we build a map of which files correspond to which
    # environments
    file_map = defaultdict(list)

    for f in files:
        parsed_filename = parse_filename(f)
        file_map[parsed_filename].append(f)

    # grab all ip / region tuples
    ip_region_pairs = set()
    for location, filepaths in file_map.items():
        for file in filepaths:
            with open(FILE_LOCATION + f'/{file}') as f:
                reader = csv.reader(f)
                for ip in get_region_ips(reader):
                    ip_region_pairs.add((ip, location))

    write_output_csv(ip_region_pairs)

if __name__ == '__main__':
    main()