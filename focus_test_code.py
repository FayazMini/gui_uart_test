from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import ImageTk, Image
import random
import threading

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
    event_counter += 1
    count = random.randint(0, 9)
    my_canvas.create_image(0, 0, image=im_Tk[count], anchor='nw')
    root.after(1000, lambda: start_image_switch())


def gui_handler_click():
    t1 = threading.Thread(target=image_click)
    t1.start()


def gui_handler_image_switch():
    t2 = threading.Thread(target=start_image_switch)
    t2.start()


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
         ImageTk.PhotoImage(image_Rabbit), ImageTk.PhotoImage(image_Squirrel)]

'''CREATING CANVAS TO DISPLAY IMAGES ON WINDOW'''
my_canvas = Canvas(root, width=490, height=300, highlightthickness=0)
my_canvas.place(x=1, y=5)

# display orbit banner as canvas background
im_bg = ImageTk.PhotoImage(image_background)
my_canvas.create_image(0, 0, image=im_bg, anchor='nw')

'''DROPDOWN MENU OPTIONS'''
var_dropmenu = StringVar()
image_labels = ["Deer", "Elephant", "Giraffe", "Gorilla", "Horse", "Lion", "Parrot", "Peacock", "Rabbit", "Squirrel"]
options = ttk.Combobox(root, textvariable=var_dropmenu)
options['values'] = image_labels
options['state'] = 'readonly'
options.place(x=10, y=10, width=100, height=20)

'''BUTTONS FOR VARIOUS OPTIONS INSIDE FRAMES'''
button_image_click = Button(root, text="CLICK", command=lambda: gui_handler_click())
button_image_click.place(x=220, y=300)

button_select_image = Button(root, text="SELECT", command=lambda: select_image())
button_select_image.place(x=10, y=50)

button_start_test = Button(root, text="START", command=lambda: gui_handler_image_switch())
button_start_test.place(x=110, y=10)

button_stop_test = Button(root, text="STOP", command=lambda: stop_test())
button_stop_test.place(x=110, y=50)

root.mainloop()
