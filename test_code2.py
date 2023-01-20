from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import random
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import serial as sr
import numpy as np
import csv

'''GLOBAL VARIABLES DECLARATION'''
cond = False
data = np.array([])
fs = 250

'''SERIAL COMMUNICATION DECLARATIONS'''
s = sr.Serial(port="/dev/cu.usbserial-0001", baudrate=115200)
s.reset_input_buffer()


def plotter():
    global data
    # print("Im here")
    i = 0
    ax.cla()  # To clear the subplot axis
    while cond:
        if s.inWaiting():
            temp1 = readData()
            temp2 = int(temp1)
            with open("test_data.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.time(), temp2])
            data = np.append(data, temp2)
            temp3 = len(data)
            if temp3 == 100 * (i + 1):  # To check the length of data array is in multiples of 100 samples
                if temp3 >= 1000:  # To check the length of data array is above or equal to 1000. We are rendering the canvas graphs after 100 ms
                    x = np.arange(start=100 * (i - 9), stop=100 * (i + 1), step=1)
                    y_temp1 = data[100 * (i - 9): 100 * (i + 1)]
                    y_temp2 = moving_average(y_temp1, 10)  # reduced number of elements.
                    y = np.append(y_temp2[0:9], y_temp2)
                    y_mean = np.mean(y)
                    y_std = np.std(y)
                    ax.set_xlim(100 * (i - 9), 100 * (i + 1))
                    ax.set_ylim(y_mean - (2 * y_std), y_mean + (2 * y_std))
                    ax.plot(x, y, color='blue')
                    canvas.draw()
                i += 1
        # print(temp3)
        # time.sleep(0.001)


def gui_handler_start():
    global cond
    cond = True
    t3 = threading.Thread(target=lambda: plotter())
    t3.start()


def gui_handler_stop():
    global cond, data
    s.reset_input_buffer()
    cond = False
    print(data)
    file = open("test_file.txt", "w")
    file.write(str(data) + "\n")
    file.close()


def readData() -> int:
    a = s.readline()
    temp = a.decode('utf-8')
    # temp2 = float(temp) * 0.0224  # Converting ADC values to uVolt
    return temp


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


'''GLOBAL VARIABLES'''
count = 0
right_score = 0
wrong_score = 0
event_counter = 0  # number of image switches in an experiment
click_counter = 0
selected_image_val = 0
image_test_start_stop_cond = False
stop_image_switch_cond = True


def image_click():
    global count, selected_image_val, right_score, wrong_score
    if count == selected_image_val:
        right_score += 1
    else:
        wrong_score += 1


def stop_test():
    global event_counter, stop_image_switch_cond
    stop_image_switch_cond = False
    print("Total number of events are: " + str(event_counter))
    print("Total number of right events are: " + str(right_score))
    print("Total number of wrong events are: " + str(wrong_score))


def select_image():
    global selected_image_val
    selected_image_val = options.current()
    print(selected_image_val)
    tkinter.messagebox.showinfo("NEUROSTELLAR", "You have selected " + str(image_labels[selected_image_val]) +
                                " for focus test")


def start_image_switch():
    global count, selected_image_val, event_counter, stop_image_switch_cond
    while stop_image_switch_cond:
        event_counter += 1
        count = random.randint(0, 9)
        Label(f_image_disp, image=im_Tk[count]).place(x=1, y=5, width=490, height=300)
        time.sleep(0.75)


def gui_handler_image_switch():
    t1 = threading.Thread(target=lambda: start_image_switch())
    t1.start()


root = Tk()
root.geometry("1200x800")
root.title("PSYCHOMETRIC TEST FOR FOCUS")

'''IMAGES FOR PSYCHOMETRIC TEST'''
image_Deer = Image.open("Deer.jpg").resize((500, 300))
image_elephant = Image.open("elephant.jpg").resize((500, 300))
image_Giraffe = Image.open("Giraffe.jpg").resize((500, 300))
image_Gorilla = Image.open("Gorilla.jpg").resize((500, 300))
image_Horse = Image.open("Horse.jpg").resize((500, 300))
image_Lion = Image.open("lion.jpg").resize((500, 300))
image_Parrot = Image.open("parrot.jpg").resize((500, 300))
image_Peacock = Image.open("Peacock.jpg").resize((500, 300))
image_Rabbit = Image.open("Rabbit.jpg").resize((500, 300))
image_Squirrel = Image.open("Squirrel.jpg").resize((500, 300))
image_background = Image.open("Orbit Banner.png").resize((500, 300))

im_Tk = [ImageTk.PhotoImage(image_Deer), ImageTk.PhotoImage(image_elephant),
         ImageTk.PhotoImage(image_Giraffe), ImageTk.PhotoImage(image_Gorilla),
         ImageTk.PhotoImage(image_Horse), ImageTk.PhotoImage(image_Lion),
         ImageTk.PhotoImage(image_Parrot), ImageTk.PhotoImage(image_Peacock),
         ImageTk.PhotoImage(image_Rabbit), ImageTk.PhotoImage(image_Squirrel),
         ImageTk.PhotoImage(image_background)]

'''FRAMES FOR VARIOUS OPTIONS INSIDE A WINDOW'''
# Defining frames for image display window
f_image_disp = LabelFrame(root, text="FOCUS TEST DISPLAY", borderwidth=2)
f_image_disp.place(x=350, y=20, width=500, height=350)

# Defining frames for graph display window
f_graph_disp = LabelFrame(root, text="EEG SIGNAL", borderwidth=2)
f_graph_disp.place(x=650, y=400, width=500, height=350)

# Defining frames for com port settings window
f_com = LabelFrame(root, text="COM PORT SETTINGS", borderwidth=2)
f_com.place(x=10, y=400, width=200, height=100)

# Defining frames for image selection settings window
f_image_settings = LabelFrame(root, text="IMAGE SELECTION FOR TEST", borderwidth=2)
f_image_settings.place(x=300, y=400, width=200, height=100)

'''CREATING CANVAS TO DISPLAY IMAGES ON WINDOW'''
# display orbit banner as canvas background
Label(f_image_disp, image=im_Tk[10]).place(x=1, y=5, width=490, height=300)

'''DROPDOWN MENU OPTIONS'''
var_dropmenu = StringVar()
image_labels = ["Deer", "Elephant", "Giraffe", "Gorilla", "Horse", "Lion", "Parrot", "Peacock", "Rabbit", "Squirrel"]
options = ttk.Combobox(f_image_settings, textvariable=var_dropmenu)
options['values'] = image_labels
options['state'] = 'readonly'
options.place(x=10, y=10, width=100, height=20)

'''BUTTONS FOR VARIOUS OPTIONS INSIDE FRAMES'''
button_image_click = Button(f_image_disp, text="CLICK", command=lambda: image_click())
button_image_click.place(x=220, y=300)

button_select_image = Button(f_image_settings, text="SELECT", command=lambda: select_image())
button_select_image.place(x=10, y=50)

button_start_test = Button(f_image_settings, text="START", command=lambda: gui_handler_image_switch())
button_start_test.place(x=110, y=10)

button_stop_test = Button(f_image_settings, text="STOP", command=lambda: stop_test())
button_stop_test.place(x=110, y=50)

fig = Figure()
ax = fig.add_subplot(111)
ax.set_xlabel('time')
ax.set_ylabel('Amplitude')

canvas = FigureCanvasTkAgg(fig, master=f_graph_disp)
canvas.get_tk_widget().place(x=5, y=5, width=480, height=300)
canvas.draw()

button_start = Button(f_com, text="START", command=lambda: gui_handler_start())
button_start.place(x=10, y=10)
button_stop = Button(f_com, text="STOP", command=lambda: gui_handler_stop())
button_stop.place(x=10, y=40)

root.mainloop()
