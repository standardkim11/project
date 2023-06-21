from tkinter import *


class Grid_Label():
    def __init__(self, master, i, j):
        self.text = StringVar()
        self.label = Label(master, textvariable=self.text, height=5, width=9,
                           relief=SOLID, bg="gray", fg="black", font="Verdana 14 bold")
        self.label.grid(row=i, column=j, sticky=W, pady=1)
        self.row = i
        self.col = j

    def change_text(self, updated_text):
        self.text.set(str(updated_text))
