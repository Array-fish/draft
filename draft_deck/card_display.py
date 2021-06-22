from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os

def card_img_frame(frame):
    img_label = ttk.Label(frame)
    explain_label = ttk.Label(frame)
    explain_text = StringVar()
    explain_label["textvariable"] = explain_text
    explain_text.set("initial text")
    initial_img = ImageTk.PhotoImage(Image.open("..\\pics\\10000.jpg"))
    img_label['image'] = initial_img
    
    # img_label.grid(column=0, row=0, sticky=(E, W))
    # explain_label.grid(column=0,row=1, sticky=(E, W))
    # img_label.columnconfigure(0, weight=1)
    # img_label.rowconfigure(0, weight=1)
    # explain_label.columnconfigure(0, weight=1)
    # explain_label.rowconfigure(0, weight=1)
    #display_card_img(label,"..\\pics\\10000.jpg")
    
    
def display_card_img(img_label,explain_text, card_id, pics_dir):
    card_img = ImageTk.PhotoImage(Image.open(os.path.join(pics_dir,card_id)+".jpg"))
    img_label.configure(img=card_img)
    explain_text.set()# get_text()