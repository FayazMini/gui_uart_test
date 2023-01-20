from tkinter import *
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
from serial.tools import list_ports
import serial as sr

dev_addr = []


def GetDevicelist():
    port = list(list_ports.comports())
    for p in port:
        dev_addr.append(p.device)
        print(p.device)


def changeState():
    global Rec_state
    Rec_state = False
    print(Rec_state)


def app():
    root = Tk()
    root.title("Neurostellar EEG Viewer")
    root.geometry("1200x800")
    # Figure properties
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()
    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)
    GetDevicelist()

    def plotter():
        global Rec_state, s
        Rec_state = True
        s = sr.Serial(clicked.get(), 115200)
        print(clicked.get())
        a = s.readline()
        temp = a.decode('utf-8')
        print(temp)
        s.reset_input_buffer()
        data = []
        print(Rec_state)
        while Rec_state:
            print("Im here")
            a = s.readline()
            temp = a.decode('utf-8')
            data.append(temp)
            print(temp)
            time.sleep(1)

    def gui_handler():
        threading.Thread(target=plotter, daemon=True).start()


    Button_start = Button(root, text="START", command=gui_handler)
    Button_start.pack(pady=20)
    Button_stop = Button(root, text="STOP", command=changeState)
    Button_stop.pack(pady=20)

    options = dev_addr
    clicked = StringVar()
    drop = OptionMenu(root, clicked, *options)
    drop.pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    app()
