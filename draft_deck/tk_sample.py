from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

root = Tk()
mainframe = ttk.Frame(root, padding="3 3 12 12").grid()
label = ttk.Label(mainframe, text='Full name:')
card_img_name = "..\\pics\\10000.jpg"
card_img = ImageTk.PhotoImage(Image.open(card_img_name))
label['image'] = card_img
label.grid()
root.mainloop()