from tkinter import *
import random
import time
import numpy as np
import threading

data = np.array([])
cond = False


def gui_handler():
    global cond
    cond = True
    t1 = threading.Thread(target=lambda: start_prog())
    t1.start()


def start_prog():
    global data, cond
    while cond:
        data = np.append(data, int(random.randint(0, 100)))
        print(data)
        time.sleep(0.5)


def stop_prog():
    global cond, data
    cond = False
    file = open("test_file.txt", "w")
    file.write(str(int(data)))
    file.close()


root = Tk()
root.geometry("600x400")
start_button = Button(root, text="START", command=lambda: gui_handler())
start_button.place(x=10, y=10)

stop_button = Button(root, text="STOP", command=lambda: stop_prog())
stop_button.place(x=10, y=50)

root.mainloop()
