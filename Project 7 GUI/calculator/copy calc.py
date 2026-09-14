import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import os

word = "hest"

root = tk.Tk()
root.title("Calculator")
root.geometry("600x600")

frame = ttk.Frame(root, padding=10)
frame.grid()

label = ttk.Label(frame, text="Nupid stigger", background="#FFFFFF")
label.grid(column=0, row=0, columnspan=4, rowspan=1, sticky="EW")

but1 = ttk.Button(frame, text="Do stuff!!", command=lambda: print(word))
but1.grid(column=0, row=1)

root.mainloop()
