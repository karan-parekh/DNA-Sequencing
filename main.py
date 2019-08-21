import threading
from queue import Queue
from general import *
from sequence import Sequence

QUEUE_FILE = 'queue.csv'
CRAWLED_FILE = 'crawled.txt'
NUMBER_OF_THREADS = 1
queue = Queue()
sequence = Sequence()


def create_threads():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        primer = queue.get()
        sequence.crawl_genome(threading.current_thread().name, primer)
        queue.task_done()


def generate_queue():
    for primer in file_to_set(QUEUE_FILE):
        queue.put(primer)
    queue.join()


def crawl():
    queued_primers = file_to_set(QUEUE_FILE)
    if len(queued_primers) > 0:
        print(str(len(queued_primers)) + ' primers in queue')
        generate_queue()


def main():
    create_threads()
    crawl()


if __name__ == '__main__':
    main()
