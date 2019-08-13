import threading
from queue import Queue
from score import *
from general import *

QUEUE_FILE = 'queue.txt'
CRAWLED_FILE = 'crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        primer = queue.get()
        crawl_genome(threading.current_thread().name, primer)
        queue.task_done()


def create_jobs():
    for primer in file_to_set(QUEUE_FILE):
        queue.put(primer)
    queue.join()
    crawl()


def crawl():
    queued_primers = file_to_set(QUEUE_FILE)
    if len(queued_primers) > 0:
        print(str(len(queued_primers)) + 'primers in queue')
        create_jobs()


create_workers()
crawl()
