import threading
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
from sequence import Sequence
from queue import Queue
from general import *


QUEUE_FILE = 'queue.csv'
CRAWLED_FILE = 'crawled.txt'
NUMBER_OF_THREADS = 10
queue = Queue()
sequence = Sequence()


# ---------- MAIN FUNCTIONS ---------- #
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


def main(event):
    if (sequence.genome_file and sequence.primers_file) is not None:
        sequence.boot()
        create_threads()
        crawl()
    else:
        print("Please select Genome and Primer files")


# ---------- GUI FUNCTIONS ---------- #
def set_genome_path():
    sequence.genome_file = askopenfile(mode='r', filetypes=[('Text file', '*.txt')]).name


def set_primers_path():
    sequence.primers_file = askopenfile(mode='r', filetypes=[('CSV file', '*.csv')]).name


def run_progress_bar(value):
    progress['value'] = value


# ---------- GUI ---------- #
root = Tk()
root.title("Primer Design")


# -------- Labels -------- #
genome_label = Label(root, text="Genome")
genome_label.grid(row=0, sticky=E, padx=2, pady=2)

primer_label = Label(root, text="Primers")
primer_label.grid(row=1, sticky=E, padx=2, pady=2)


# -------- Buttons -------- #
genome_path = Button(root, text="Choose file (.txt)", command=set_genome_path)
genome_path.grid(row=0, column=1, columnspan=2, padx=2, pady=2)

primer_path = Button(root, text="Choose file (.csv)", command=set_primers_path)
primer_path.grid(row=1, column=1, columnspan=2, padx=2, pady=2)

start = Button(root, text="DESIGN")
start.bind("<Button -1>", main)
start.grid(row=2, column=1, columnspan=1, padx=2, pady=2)

# -------- Progress Bar -------- #
progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
progress.grid(row=7, columnspan=3, padx=2, pady=2)


root.mainloop()
