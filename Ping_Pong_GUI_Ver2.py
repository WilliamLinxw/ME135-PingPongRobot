
# coding: utf-8

# In[ ]:


import matplotlib
import matplotlib.backends.backend_tkagg
# from gi.repository import Gtk
# import matplotlib as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import numpy

import tkinter as tk
from tkinter import ttk

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt


LARGE_FONT= ("Times New Roman", 50)
NORM_FONT= ("Times New Roman", 40)
SMALL_FONT= ("Times New Roman", 30)
style.use("ggplot")

f = Figure()
a = f.add_subplot(211)
b = f.add_subplot(212)

g = Figure()
c = g.add_subplot(221)
d = g.add_subplot(223)
e = g.add_subplot(222)
h = g.add_subplot(224)



def popupmsg(msg):
    popup = tk.Tk()
    
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg,font=SMALL_FONT)
    label.pack(side="top",fill="x",pady=10)
    B1 = ttk.Button(popup, text = "Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    
        
def animatea(i):
    pullData = open("sampleData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    zList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,z=eachLine.split(',')
            xList.append(int(x))
            zList.append(int(z))
    a.clear()

    length = len(xList)
    intv = 16*10**(-3)
    t = numpy.linspace(0,length-1,length)*intv
    a.plot(t,xList, marker="o")
    
    title = "Horizontal movement of the BOT"
    ylabel = "X Position (mm)"
    a.set_title(title)
    a.set_ylabel(ylabel)
    
def animateb(i):
    pullData = open("sampleData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    zList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,z=eachLine.split(',')
            xList.append(int(x))
            zList.append(int(z))
    b.clear()
    
    length = len(xList)
    intv = 16*10**(-3)
    t = numpy.linspace(0,length-1,length)*intv
    b.plot(t,zList, marker="o")
    

    
    title = "Vertical movement of the BOT"
    xlabel = "Time (s)"
    ylabel = "Z Position (mm)"
    b.set_title(title)
    b.set_xlabel(xlabel)
    b.set_ylabel(ylabel)
    
def animatec(i):
    pullData = open("sampleData-Copy1.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y=eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    c.clear()
    
    c.plot(xList,yList,marker="o")
    c.plot(xList,xList,marker="o")
    
    title = "x-y Chart of the Ping Pong"
    xlabel = "X Position (mm)"
    ylabel = "Y Position (mm)"
    c.set_title(title)
    c.set_ylabel(ylabel)

def animated(i):
    pullData = open("sampleData-Copy1.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y=eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    d.clear()
    
    d.plot(xList,yList,marker="o")
    d.plot(xList,xList,marker="o")
    
    title = "x-z Chart of the Ping Pong"
    xlabel = "X Position (mm)"
    ylabel = "Z Position (mm)"
    d.set_title(title)
    d.set_ylabel(ylabel)
    
def animatee(i):
    pullData = open("sampleData-Copy1.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y=eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    e.clear()

    
    e.plot(xList,yList,marker="o")
    e.plot(xList,xList,marker="o")
    
    title = "y-z Chart of the Ping Pong"
    xlabel = "Y Position (mm)"
    ylabel = "Z Position (mm)"
    e.set_title(title)
    e.set_ylabel(ylabel)

def animateh(i):
    pullData = open("sampleData-Copy1.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y=eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    h.clear()

    
    h.plot(xList,yList,marker="o")
    h.plot(xList,xList,marker="o")
    
    title = "x-z Chart of the Prediction"
    xlabel = "X Position (mm)"
    ylabel = "Z Position (mm)"
    h.set_title(title)
    h.set_ylabel(ylabel)


class PiongPongBotGUI(tk.Tk):

        

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "PongPongBot GUI")
        #tk.Tk.iconbitmap (self, default="")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar=tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Setting", command=lambda:popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command =quit)
        menubar.add_cascade(label="File",menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        
        for F in (StartPage,PageOne,PageTwo,PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    

    def client_exit(self):
        exit()



def qf(param):
    print(param)
    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="""Ping Pong Bot GUI 
        Do you agree to gurantee us an A?""", font=LARGE_FONT)
        label.pack(pady=100,padx=100)
        
        button1 = ttk.Button(self, text="Agree", 
                            command=lambda:controller.show_frame(PageOne))
        button1.pack()
        
        button2 = ttk.Button(self, text="Disagree", 
                            command=lambda:controller.show_frame(PageOne))
        button2.pack() 

        
class PageOne (tk.Frame):
    
    def __init__ (self,parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=100,padx=100)
        
        button1 = ttk.Button(self, text="Ball Trajectory Tracking", 
                            command=lambda:controller.show_frame(PageTwo))
        button1.pack()
    
        button2 = ttk.Button(self, text="BOT Movement Tracking", 
                            command=lambda:controller.show_frame(PageThree))
        button2.pack() 
        
class PageTwo (tk.Frame):
    
    def __init__ (self,parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Trajectory Tracking Charts", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self, text="Back to Home Page", 
                            command=lambda:controller.show_frame(PageOne))
        button1.pack()
        
        canvas=FigureCanvasTkAgg(g,self)
        # canvas.show
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
class PageThree (tk.Frame):
    
    def __init__ (self,parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BOT Movement Tracking Charts", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self, text="Back to Home Page", 
                            command=lambda:controller.show_frame(PageOne))
        button1.pack()
        

        
        canvas=FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
app = PiongPongBotGUI()
app.geometry("1920x1080")
ani = animation.FuncAnimation(f, animatea, interval=1000)
anib = animation.FuncAnimation(f, animateb, interval=1000)
anic = animation.FuncAnimation(g, animatec, interval=1000)
anie = animation.FuncAnimation(g, animatee, interval=1000)
anid = animation.FuncAnimation(g, animated, interval=1000)
anih = animation.FuncAnimation(g, animateh, interval=1000)
app.mainloop()

