import csv
import threading
from queue import Queue
from sequence import Sequence
from general import *


QUEUE_FILE = 'queue.csv'
CRAWLED_FILE = 'crawled.txt'
NUMBER_OF_THREADS = 4
queue = Queue()
Sequence()


def populate_queue():
    with open('primers/primers.csv', 'r') as p:
        primers = csv.DictReader(p)

        with open('queue.csv', 'w') as q:
            fieldnames = ['name', 'sequence']
            csv_writer = csv.DictWriter(q, fieldnames=fieldnames)
            csv_writer.writeheader()
            next(primers)
            for primer in primers:
                d = {'name': primer['name'], 'sequence': primer['sequence']}
                csv_writer.writerow(d)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        primer = queue.get()
        Sequence.crawl_genome(threading.current_thread().name, primer)
        queue.task_done()


def create_jobs():
    for primer in file_to_set(QUEUE_FILE):
        queue.put(primer)
    queue.join()
    print(queue.get())
    crawl()


def crawl():
    queued_primers = file_to_set(QUEUE_FILE)
    if len(queued_primers) > 0:
        print(str(len(queued_primers)) + 'primers in queue')
        create_jobs()


if __name__ == "__main__":
    populate_queue()
    create_workers()
    crawl()
