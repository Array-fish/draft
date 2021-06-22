from tkinter import StringVar, ttk, N,S,E,W
import os
import pandas as pd
from drafter import drafter

class card_detail_frame(ttk.Frame):
    def __init__(self,master,drafter):
        super().__init__(master)
        # variable
        self.display_img = 0
        self.card_detail = StringVar()
        self.drafter = drafter
        # card_label
        self.img_label = ttk.Label(master)
        self.img_label.grid(column =0,row=0,sticky=(N,S,E,W))
        self.img_label.columnconfigure(0,weight=1)
        self.img_label.rowconfigure(0,weight=1)
        # text_label
        self.detail_label = ttk.Label(master,textvariable=self.card_detail)
        self.detail_label.grid(column =1,row=0,sticky=(N,S,E,W))
        self.detail_label.columnconfigure(0,weight=1)
        self.detail_label.rowconfigure(0,weight=1)

    def display_card(self,img):
        self.display_img =  img
        self.img_label.configure(img=self.display_img)

    

    def set_card_detail(self,card_data_dict):
        tmp_explain_text = "["
        for type in card_data_dict["type"]:
            tmp_explain_text = tmp_explain_text + type + "|"
        tmp_explain_text += "]"
        tmp_explain_text += card_data_dict["race"]+"/"+card_data_dict["attribute"]+"\n"
        tmp_explain_text += "[★"+card_data_dict["level"]+"]"+card_data_dict["atk"]+"/"+card_data_dict["def"]+"\n"
        tmp_explain_text += card_data_dict["text"]
        self.card_detail.set(tmp_explain_text)
    
    # public
    def update_card_display(self,card_id):
        self.display_card(self.drafter.get_card_img())
        card_dict = self.drafter.get_card_data(card_id)
        self.set_card_detail(card_dict)


