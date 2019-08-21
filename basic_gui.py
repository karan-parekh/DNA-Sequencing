import threading
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
from sequence import Sequence
from queue import Queue
from general import *


QUEUE_FILE = 'queue.csv'
CRAWLED_FILE = 'crawled.txt'
NUMBER_OF_THREADS = 1
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
    print("Running main")
    sequence.boot()
    create_threads()
    crawl()


# ---------- GUI FUNCTIONS ---------- #
def set_genome_path():
    sequence.genome_file = askopenfile().name


def set_primers_path():
    sequence.primers_file = askopenfile().name


def set_genome_name_sequence(event):
    print("Running set_genome_name_sequence")
    _ = genome_name_entry.get()  # for later use
    seq = genome_sequence_entry.get()
    sequence.genome = seq
    genome_name_entry.delete(0, 'end')
    genome_sequence_entry.delete(0, 'end')


def get_primer_name_sequence(event):
    print("Running get_primer_name_sequence")
    sequence.custom_primers = True
    name = primer_name_entry.get()
    seq = primer_sequence_entry.get()
    append_to_csv("primers/custom_primers.csv", name, seq)
    primer_name_entry.delete(0, 'end')
    primer_sequence_entry.delete(0, 'end')


def run_progress_bar(value):
    progress['value'] = value


# ---------- GUI ---------- #
root = Tk()
root.title("Primer Design")


# -------- Labels -------- #
genome_label = Label(root, text="Genome")
genome_label.grid(row=0, sticky=E, padx=2, pady=2)

primer_label = Label(root, text="Primers")
primer_label.grid(row=3, sticky=E, padx=2, pady=2)

or_label_g = Label(root, text="OR")
or_label_g.grid(row=1, column=0, columnspan=2, padx=2, pady=2)

or_label_p = Label(root, text="OR")
or_label_p.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

# -------- Text boxes -------- #
genome_name_entry = Entry(root)
genome_name_entry.insert(0, 'Name')
genome_name_entry.grid(row=0, column=1)

genome_sequence_entry = Entry(root)
genome_sequence_entry.insert(0, 'Sequence')
genome_sequence_entry.bind("<Return>", set_genome_name_sequence)
genome_sequence_entry.grid(row=0, column=2)

primer_name_entry = Entry(root)
primer_name_entry.insert(0, 'Name')
primer_name_entry.grid(row=3, column=1)

primer_sequence_entry = Entry(root)
primer_sequence_entry.insert(0, 'Sequence')
primer_sequence_entry.bind("<Return>", get_primer_name_sequence)
primer_sequence_entry.grid(row=3, column=2)

# -------- Buttons -------- #
genome_path = Button(root, text="Choose file (.txt)", command=set_genome_path)
genome_path.grid(row=2, column=0, columnspan=2, padx=2, pady=2)

primer_path = Button(root, text="Choose file (.csv)", command=set_primers_path)
primer_path.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

start = Button(root, text="DESIGN")
start.bind("<Button -1>", main)
start.grid(row=6, column=2, columnspan=1, padx=2, pady=2)

# -------- Progress Bar -------- #
progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='indeterminate')
progress.grid(row=7, columnspan=3, padx=2, pady=2)


root.mainloop()
