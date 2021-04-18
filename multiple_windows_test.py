import tkinter as tk
from tkinter import *

class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        # b1 = tk.Button(self, text="Add another window", command = self.newWindow)
        self.count = 0
        self.canvas1 = Canvas(self, width=500, height=500)
        b1 = tk.Button(self.canvas1, text="Add another window", command = self.create_new_window)
        # b1.pack(side="top", padx=40, pady=40)
        self.canvas1.pack(side="top")
        b1.pack(side="top", padx=250, pady=240)

        self.window1 = tk.Toplevel(self)
        self.window1.geometry("+930+300")
        self.canvas1 = Canvas(self.window1, width=200, height=500)
        tk.Label(self.window1, text="This is window 1", bg='green').pack(expand=1, fill=tk.Y)
        self.canvas1.pack(side="top", fill="both")

        self.window2 = tk.Toplevel(self)
        self.window2.geometry("+90+300")
        self.canvas2 = Canvas(self.window2, width=200, height=500)
        tk.Label(self.window2, text="This is window 2", bg='red').pack(expand=1, fill=tk.Y)
        self.canvas2.pack(side="top", fill="both")


    def create_new_window(self):
        self.window1 = tk.Toplevel(self)
        self.window1.geometry("+160+300")
        self.canvas1 = Canvas(self.window1, width=50, height=500)
        # label = tk.Label(self.window1, text="This is window #%s" % self.count)
        self.canvas1.pack(side="top", fill="both")

    def create_new_window2(self):
        self.window2 = tk.Toplevel(self)
        self.canvas2 = Canvas(self.window2, width=500, height=500)
        # label = tk.Label(self.window2, text="This is window #%s" % self.count)
        self.canvas2.pack(side="top", fill="both", expand=True, padx=40, pady=40)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("+300+300")
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()