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

#================================Speed gauge functions==========================================
def degree_range(n): 
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points
    
def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation
    
def gauge(labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], colors='jet_r', arrow=1, title='', ax=None): 
    
    """
    some sanity checks first
    
    """
    
    N = len(labels)
    
    if arrow > N: 
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow, N))
 
    
    """
    if colors is a string, we assume it's a matplotlib colormap
    and we discretize in N discrete colors 
    """
    
    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list): 
        if len(colors) == N:
            colors = colors[::-1]
        else: 
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors), N))

    """
    begins the plotting
    """
    
    #fig, ax = plt.subplots()

    ang_range, mid_points = degree_range(N)

    labels = labels[::-1]
    
    """
    plots the sectors and the arcs
    """
    patches = []
    for ang, c in zip(ang_range, colors): 
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
    
    [ax.add_patch(p) for p in patches]

    
    """
    set the labels (e.g. 'LOW','MEDIUM',...)
    """

    for mid, lab in zip(mid_points, labels): 

        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=8, \
            fontweight='bold', rotation = rot_text(mid))

    """
    set the bottom banner and the title
    """
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
    ax.add_patch(r)
    
    ax.text(0, -0.05, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=22, fontweight='bold')

    """
    plots the arrow now
    """
    
    pos = mid_points[abs(arrow - N)]
    
    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

    """
    removes frame and ticks, and makes axis equal and tight
    """
    
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    # plt.tight_layout()
    return ax
#===============================================================================================

#==============================================battery==========================================
def battery(level_reading_l=0, level_reading_r=0, ax=None):
    if level_reading_l > 100.0:
        level_reading_l = 100.0
    if level_reading_l < 0.0:
        level_reading_l = 0.0
    if level_reading_r > 100.0:
        level_reading_r = 100.0
    if level_reading_r < 0.0:
        level_reading_r = 0.0
    N = 2
    level_reading = (level_reading_l, level_reading_r)
    ind = np.arange(N)
    width = 0.35
    ax.bar(['left', 'right'], level_reading, width, color=((((100-level_reading_l)/100.0),(level_reading_l/100.0),0.0), (((100-level_reading_r)/100.0),(level_reading_r/100.0),0.0)))
    for index, value in enumerate(level_reading):
        ax.text(index - 0.05, value + 1, str(value), color='blue', fontweight='bold')
    ax.set_ylabel('percentage')
    ax.set_title('battery level')
    ax.set_yticks(np.arange(0, 101, 10))
    return ax
#===============================================================================================

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

orange_bkg = '#ffcc99'
blue_bkg = '#99ccff'

HEIGHT=400
WIDTH=400

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

#==============================================plot for center screen==============================================================================
f = Figure(figsize=(25,25), dpi=100)
a = f.add_subplot(2,2,4)
b = f.add_subplot(2,2,1)
c = f.add_subplot(2,2,3)
e = f.add_subplot(2,2,2)

g = Figure(figsize=(25,25), dpi=100)
h = g.add_subplot(2,2,1)

track_image = plt.imread("purdue_race_track.jpg")
e.imshow(track_image)
e.grid(False)
gauge(labels=['0','10','20','30','40','50','60'], colors='RdBu', arrow=7, title='NIWA ENSO TRACKER', ax=b)
battery(level_reading_l=30, level_reading_r=10, ax=h)



def animate(i):
    pullData = open("sampleData.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
            
    a.clear()
    a.plot(xList, yList)
    
    pullData = open("mph.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x= eachLine.split()[0]
            xList.append(float(x))
    cur_mph = xList[len(xList) - 1]
    b.clear()
    gauge(labels=['0','5','10','15','20','25','30','35','40','45','50','55','60'], colors='RdBu', arrow=int(cur_mph)//5 + 1, title=str(cur_mph) + ' mph', ax=b)
    
    pullData = open("track_coordinates.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    if len(xList) > 0 and len(yList) > 0:
        e.clear()
        e.imshow(track_image)
        e.grid(False)
        e.scatter([xList[len(xList) - 1]], [yList[len(yList) - 1]], c='r', s=40)
        
    pullData = open("battery_status.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
            
    if len(xList) > 0 and len(yList) > 0:
        h.clear()
        battery(xList[len(xList) - 1], yList[len(yList) - 1], ax=h)
        
    input_frame = plt.imread("frame.jpg")
    c.imshow(input_frame)
    c.grid(False)
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
        
        for F in (StartPage, PageOne, PageTwo, PageThree):
            
        
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
    def NewSideScreenOne(self):      
        self.root_new_Side_Screen_One = tk.Tk()
        container = tk.Frame(self.root_new_Side_Screen_One)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame = PageOne(container, self.root_new_Side_Screen_One)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()     
        ani1 = animation.FuncAnimation(g, animate, interval=500)
        self.root_new_Side_Screen_One.mainloop()
        
    def NewSideScreenTwo(self):      
        self.root_new_Side_Screen_Two = tk.Tk()
        container = tk.Frame(self.root_new_Side_Screen_Two)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame = PageTwo(container, self.root_new_Side_Screen_Two)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()      
        self.root_new_Side_Screen_Two.mainloop()
        
    def NewCenterScreen(self):      
        self.root_new_Center_Screen = tk.Tk()
        container = tk.Frame(self.root_new_Center_Screen)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame = PageThree(container, self.root_new_Center_Screen)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()  
        ani = animation.FuncAnimation(f, animate, interval=500)
        self.root_new_Center_Screen.mainloop()
        
def qf(param):
    print(param)           
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="UCSD ev Grand Prix Control Station", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self, text="Side Screen 1", command=lambda: controller.NewSideScreenOne())
        button1.pack()
        
        button2 = ttk.Button(self, text="Side Screen 2", command=lambda: controller.NewSideScreenTwo())
        button2.pack()
        
        button3 = ttk.Button(self, text="Center Screen", command=lambda: controller.NewCenterScreen())
        button3.pack()
        
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Side Screen One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # button1 = ttk.Button(self, text="Back to Home", command=lambda: qf("TEST"))
        # button1.pack()
        
        # button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        # button2.pack()
        
        canvas = FigureCanvasTkAgg(g, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Side Screen Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        # button1.pack()
        
        # button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        # button2.pack()
        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Center Screen!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # button1 = ttk.Button(self, text="Back to Home", command=lambda: qf("TEST"))
        # button1.pack()
        
        # button1 = ttk.Button(self, text="Side Screen 1", command=lambda: controller.NewSideScreenOne())
        # button1.pack()
        
        # button2 = ttk.Button(self, text="Side Screen 2", command=lambda: controller.NewSideScreenTwo())
        # button2.pack()
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
app = Control_Station()
# ani = animation.FuncAnimation(f, animate, interval=500)
# ani1 = animation.FuncAnimation(g, animate, interval=500)
app.mainloop()