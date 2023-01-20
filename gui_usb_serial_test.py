from tkinter import *
from random import randint
import serial as sr
from serial.tools import list_ports

# these two imports are important 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading

continuePlotting = False

port = list(list_ports.comports())
for p in port:
    print(p.device)

global device_name
if "usbserial" in p.device:
    device_name = '/dev/cu.usbserial-0001'
    print("Available")
else:
    print("device not available")


data = []



def read_Data():
    a = s.readline()
    temp = a.decode('utf-8')
    data.append(temp)
    print(temp)
    return data

def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True


def app():
    # initialise a window. 
    root = Tk()
    root.config(background='white')
    root.geometry("1000x700")

    lab = Label(root, text="Live Plotting", bg='white').pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            #dpts = data_points()
            dpts = read_Data()
            #ax.plot(range(10), dpts, marker='o', color='orange')
            ax.plot(dpts)
            graph.draw()
            time.sleep(0.05)

    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()

    root.mainloop()


if __name__ == '__main__':
    app()
