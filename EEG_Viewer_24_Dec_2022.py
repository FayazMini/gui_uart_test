from tkinter import *
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import serial as sr
import time
import numpy as np
from scipy.signal import butter, lfilter

'''GLOBAL VARIABLES DECLARATION'''
cond = False
data = np.array([])
fs = 250
'''
f1 = 2
f2 = 30
wn1 = f1 / (fs / 2)
wn2 = f2 / (fs / 2)
filt_order = 3

b, a = butter(filt_order, wn2, fs=fs, btype='low')
print("Hello mini")
'''
'''SERIAL COMMUNICATION DECLARATIONS'''
s = sr.Serial(port="/dev/cu.usbserial-0001", baudrate=115200)
s.reset_input_buffer()


def plotter():
    global data
    print("Im here")
    i = 0
    data = []
    ax.cla()  # To clear the subplot axis
    while cond:
        if s.inWaiting():
            temp1 = readData()
            temp2 = int(temp1)
            data = np.append(data, temp2)
            temp3 = len(data)
            if temp3 == 100 * (i + 1):  # To check the length of data array is in multiples of 100 samples
                if temp3 >= 1000:  # To check the length of data array is above or equal to 1000. We are rendering the canvas graphs after 100 ms
                    x = np.arange(start=100 * (i - 9), stop=100 * (i + 1), step=1)
                    y_temp1 = data[100 * (i - 9): 100 * (i + 1)]
                    y_temp2 = moving_average(y_temp1,
                                             10)  # reduced number of elements. To compensate we have appended extra elements
                    y = np.append(y_temp2[0:9], y_temp2)
                    # print(y)
                    y_mean = np.mean(y)
                    y_std = np.std(y)
                    ax.set_xlim(100 * (i - 9), 100 * (i + 1))
                    ax.set_ylim(y_mean - (2 * y_std), y_mean + (2 * y_std))
                    ax.plot(x, y, color='blue')
                    canvas.draw()
                i += 1
        # print(temp3)
        # time.sleep(0.001)


def plot_cond_checker():
    global cond
    if cond == True:
        cond = False
    else:
        cond = True


def gui_handler():
    plot_cond_checker()
    t1 = threading.Thread(target=lambda: plotter())
    t1.start()


def readData() -> int:
    a = s.readline()
    temp = a.decode('utf-8')
    # temp2 = float(temp) * 0.0224  # Converting ADC values to uVolt
    return temp


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


'''GUI TKINTER CODE'''

root = Tk()
root.title("Serial Communication")
root.geometry("1200x800")

fig = Figure()
ax = fig.add_subplot(111)
ax.set_xlabel('time')
ax.set_ylabel('Amplitude')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=50, y=20, width=1000, height=400)
canvas.draw()

button_start = Button(root, text="START", command=lambda: gui_handler())
button_start.place(x=50, y=500)
button_stop = Button(root, text="STOP", command=lambda: gui_handler())
button_stop.place(x=150, y=500)

root.mainloop()
