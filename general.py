import os
import csv
from functools import wraps
from time import time


def measure_time(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(f"Total execution time: {end_ if end_ > 0 else 0} ms")
    return _time_it


def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files():
    queue = os.path.join('queue.csv')
    crawled = os.path.join('crawled.txt')
    results = os.path.join('results.csv')
    if not os.path.isfile(queue):
        write_file(queue, '')
    if not os.path.isfile(crawled):
        write_file(crawled, '')

    with open(results, 'w') as file:
        fieldnames = (
            'name',
            'sequence',
            'direction',
            'length',
            'match',
            'mismatch',
            'coordinate (start)',
            'coordinate (end)'
        )
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()

    with open('primers/custom_primers.csv', 'w') as file:
        fieldnames = ('name', 'sequence')
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


def append_to_csv(path, *args, fieldnames=("name", "sequence")):
    name, seq = args
    with open(path, 'a') as file:
        fieldnames = fieldnames
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        row = {'name': name, 'sequence': seq}
        csv_writer.writerow(row)


def append_to_results(*args):
    name, match, direction = args
    score, _, query, subject_start, _, length = match.values()
    with open("results.csv", 'a') as file:
        fieldnames = (
            'name',
            'sequence',
            'direction',
            'length',
            'match',
            'mismatch',
            'coordinate (start)',
            'coordinate (end)'
        )
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        row = {
            'name': name,
            'sequence': query,
            'direction': direction,
            'length': length,
            'match': score,
            'mismatch': length - score,
            'coordinate (start)': subject_start,
            'coordinate (end)': subject_start + length
            }
        csv_writer.writerow(row)


# Delete the contents of a file
def delete_file_contents(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l+"\n")