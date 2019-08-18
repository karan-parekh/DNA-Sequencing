from tkinter import *
from tkinter.filedialog import askopenfile
from main import *


def open_file(event):
    file_path = askopenfile().name
    print(file_path)


def get_primer_name(event):
    print("Running get_primer_name")


def get_genome_name(event):
    print("Running get_genome_name")


root = Tk()
root.title("Primer Design")

# -------- FRAMES -------- #
top = Frame

genome_label = Label(root, text="Genome")
primer_label = Label(root, text="Primers")
or_label_g = Label(root, text="OR")
or_label_p = Label(root, text="OR")

genome_name_entry = Entry(root)
genome_name_entry.insert(0, 'Enter Name')

genome_sequence_entry = Entry(root)
genome_sequence_entry.insert(0, 'Enter Sequence')

primer_name_entry = Entry(root)
primer_name_entry.insert(0, 'Enter Name')
primer_name_entry.bind("<Return>", )

primer_sequence_entry = Entry(root)
primer_sequence_entry.insert(0, 'Enter Sequence')

genome_path = Button(root, text="Choose file (.txt)", command=open_file)
primer_path = Button(root, text="Choose file (.csv)", command=open_file)

genome_label.grid(row=0, sticky=E, padx=2, pady=2)
primer_label.grid(row=3, sticky=E, padx=2, pady=2)

or_label_g.grid(row=1, column=0, columnspan=2, padx=2, pady=2)
or_label_p.grid(row=4, column=0, columnspan=2, padx=2, pady=2)


genome_name_entry.grid(row=0, column=1)
primer_name_entry.grid(row=3, column=1)

genome_sequence_entry.grid(row=0, column=2)
primer_sequence_entry.grid(row=3, column=2)

genome_path.grid(row=2, column=0, columnspan=2, padx=2, pady=2)
primer_path.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

start = Button(root, text="DESIGN")
start.grid(row=6, column=2, columnspan=1, padx=2, pady=2)

root.mainloop()
