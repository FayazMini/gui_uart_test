from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
import threading

count = 0

root = Tk()
root.geometry("800x600")

im1 = Image.open("Orbit Banner.png").resize((600, 400))
im2 = Image.open("FINAL brochure 2.png").resize((600, 400))

im_Tk = [ImageTk.PhotoImage(im1),
         ImageTk.PhotoImage(im2)]

my_canvas = Canvas(root, width=600, height=400, highlightthickness=0)
my_canvas.place(x=50, y=10)

# display first image as canvas background
my_canvas.create_image(0, 0, image=im_Tk[0], anchor='nw')

start_Button = Button(root, text="START", command=lambda: image_switch())
start_Button.place(x=50, y=450)

click_Button = Button(root, text="CLICK", command=lambda: gui_handler())
click_Button.place(x=150, y=450)

var = StringVar()
click_answer_label = Label(root, textvariable=var)
click_answer_label.place(x=250, y=450)

image_options = ["dog", "cat", "peacock"]
var1 = StringVar()
options = ttk.Combobox(root, textvariable=var1)
options['values'] = image_options
options['state'] = 'readonly'
options.place(width=100, height=20, x=350, y=450)


def options_selected():
    print("selected option is: " + str(options.current()))


def image_switch():
    global count
    count = random.randint(0, 1)
    print(count)
    my_canvas.create_image(0, 0, image=im_Tk[count], anchor='nw')
    root.after(2000, lambda: image_switch())


def click_answer():
    var.set("The clicked answer is " + str(count))


def gui_handler():
    options_selected()
    t1 = threading.Thread(target=lambda: click_answer())
    t1.start()


root.mainloop()
