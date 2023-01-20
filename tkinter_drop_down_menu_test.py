import serial as sr
from serial.tools import list_ports
from tkinter import *
import time

dev_addr = []
def GetDevicelist():
    port = list(list_ports.comports())
    for p in port:
        dev_addr.append(p.device)
        print(p.device)


def connect():
    s = sr.Serial(clicked.get(), 115200)
    print(clicked.get())
    s.reset_input_buffer()
    data = []
    while True:
        a = s.readline()
        temp = a.decode('utf-8')
        data.append(temp)
        print(temp)
        time.sleep(1)


GetDevicelist()
root = Tk()
root.geometry('1200x800')
print("hello")
print(dev_addr)
options = dev_addr
clicked = StringVar()
drop = OptionMenu(root, clicked, *options)
drop.pack(pady=20)
Button_Connect = Button(root, text="CONNECT", command=connect)
Button_Connect.pack(pady=20)
root.mainloop()
