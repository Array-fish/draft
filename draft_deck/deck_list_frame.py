from tkinter import StringVar, ttk,N,S,W,E
import tkinter
from tkinter.constants import VERTICAL
from drafter import Drafter
class Deck_list_frame(ttk.Frame):
    def __init__(self, master,drafter):
        super().__init__(master)
        self.drafter = drafter
        self.cards_var = StringVar()
        #self.cards_name = list()
        #self.cards_id = list()

        self.deck_list_box = tkinter.Listbox(master,listvaribale = self.cards_var,height = 10)
        self.deck_list_box.grid(column=0,row=0,sticky=(N,S,W,E))
        self.deck_list_box.columnconfigure(0,weight = 0)
        self.deck_list_box.rowconfigure(0, weight=1)

        self.deck_scrollbar = ttk.Scrollbar(master,orient=VERTICAL, command=self.deck_list_box.yview)
        self.deck_scrollbar.grid(column=1,row=0,sticky=(N,S))
        self.deck_list_box["yscrollcommand"] = self.deck_scrollbar.set
        self.register_cards_var()

    def add_cards(self, cards_list):
        self.cards_name += cards_list
        self.cards_var.set(self.cards_name)

    def register_cards_var(self):
        self.drafter.set_cards_var(self.cards_var)
