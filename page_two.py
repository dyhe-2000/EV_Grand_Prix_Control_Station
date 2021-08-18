import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np

from matplotlib.patches import Circle, Wedge, Rectangle

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

orange_bkg = '#ffcc99'
blue_bkg = '#99ccff'

HEIGHT=400
WIDTH=400

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

#==============================================plot for side screen two==============================================================================    
side_screen_two = Figure(figsize=(25,25), dpi=100)
two_one = side_screen_two.add_subplot(2,2,1)
two_two = side_screen_two.add_subplot(2,2,2)
two_three = side_screen_two.add_subplot(2,2,3)
two_four = side_screen_two.add_subplot(2,2,4)

two_one.set_title('speed vs time')
two_two.set_title('throttle(%) vs time')
two_three.set_title('break(%) vs time')
two_four.set_title('motor and ESC temperature(C) vs time')

def animate_side_two(i):
    pullData = open("speed.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    two_one.clear()
    two_one.set_title('speed vs time')
    two_one.plot(xList, yList)
    
    pullData = open("throttle.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    two_two.clear()
    two_two.set_title('throttle(%) vs time')
    two_two.plot(xList, yList)
    
    pullData = open("break.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    two_three.clear()
    two_three.set_title('break(%) vs time')
    two_three.plot(xList, yList)
    
    pullData = open("temp.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    two_four.clear()
    two_four.set_title('motor and ESC temperature(C) vs time')
    two_four.plot(xList, yList)
    
#========================================================================================================================================================

class Control_Station(tk.Tk):
    
    def __init__(self, *args, **kwargs):
    
        tk.Tk.__init__(self, *args, **kwargs)
        
        # tk.Tk.iconbitmap(self, default=".ico")
        tk.Tk.wm_title(self, "UCSD ev Grand Prix Control Station")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageTwo):
            
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
    def NewSideScreenTwo(self):  
        self.root_new_Side_Screen_Two = tk.Tk()
        container = tk.Frame(self.root_new_Side_Screen_Two)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame = PageTwo(container, self.root_new_Side_Screen_Two)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()    
        ani2 = animation.FuncAnimation(side_screen_two, animate_side_two, interval=100)
        self.root_new_Side_Screen_Two.mainloop()
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="UCSD ev Grand Prix Control Station", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button2 = ttk.Button(self, text="Side Screen 2", command=lambda: controller.NewSideScreenTwo())
        button2.pack()
        
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Side Screen Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        # button1.pack()
        
        # button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        # button2.pack()
        
        canvas = FigureCanvasTkAgg(side_screen_two, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
app = Control_Station()
# ani = animation.FuncAnimation(f, animate, interval=500)
# ani1 = animation.FuncAnimation(g, animate, interval=500)
app.mainloop()