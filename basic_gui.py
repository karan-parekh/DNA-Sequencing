from tkinter import *
from tkinter.filedialog import askopenfile


def open_file():
    return askopenfile().name


root = Tk()
root.title("Primer Design")

genome_label = Label(root, text="Genome File (.txt)")
primer_label = Label(root, text="Primers File (.csv)")

genome_label.grid(row=0, sticky=E, padx=2, pady=2)
primer_label.grid(row=1, sticky=E, padx=2, pady=2)

genome_path = Button(root, text="Choose file", command=open_file)
primer_path = Button(root, text="Choose file", command=open_file)

genome_path.grid(row=0, column=1, padx=2, pady=2)
primer_path.grid(row=1, column=1, padx=2, pady=2)

start = Button(root, text="DESIGN")
start.grid(columnspan=2, padx=2, pady=2)

root.mainloop()
