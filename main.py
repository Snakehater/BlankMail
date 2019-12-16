from mttkinter import mtTkinter as tk
from tkinter import ttk
import smtplib

def send(arg):
    pass

root = tk.Tk()
root.title("Stylish Mail")


tk.Label(root, height=1, width=5, text='From').grid(column=0, row=0)
mailFromEntry = tk.Entry(root, width=35)
mailFromEntry.grid(column=1, row=0, padx=10)

tk.Label(root, height=1, width=5, text='To').grid(column=0, row=1)
mailToEntry = tk.Entry(root, width=35)
mailToEntry.grid(column=1, row=1, padx=10)

tk.Label(root, text='Message:', height=1).grid(padx=10, row=2, sticky='ew', columnspan=2)

inputText = tk.Text(root, width=40, height=20, highlightthickness='0', borderwidth=2, relief="sunken")
inputText.grid(column=0, row=3, columnspan=2, padx=10, sticky='ew')

sendBtn = ttk.Button(root, text='Send', command=(lambda: send()))
sendBtn.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky='ew')

tk.mainloop()
