from tkinter import StringVar, ttk, N, S, W, E
import tkinter
from tkinter.constants import VERTICAL


# from drafter import Drafter
class DeckListFrame(ttk.Frame):
    def __init__(self, master, drafter, detail_controller):
        super().__init__(master)
        self.drafter = drafter
        self.cards_var = StringVar()
        self.detail_controller = detail_controller

        self.deck_list_box = tkinter.Listbox(self, listvariable=self.cards_var, height=40, selectmode="single")
        self.deck_list_box.grid(column=0, row=0, sticky=(N, S, W, E))
        self.deck_list_box.columnconfigure(0, weight=0)
        self.deck_list_box.rowconfigure(0, weight=1)
        self.deck_list_box.bind("<<ListboxSelect>>", lambda e: self.show_detail())

        self.deck_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.deck_list_box.yview)
        self.deck_scrollbar.grid(column=1, row=0, sticky=(N, S))
        self.deck_list_box["yscrollcommand"] = self.deck_scrollbar.set
        self.register_cards_var()

    def register_cards_var(self):
        self.drafter.set_cards_var(self.cards_var)

    def show_detail(self):
        if self.cards_var.get() != "":
            selected_id = self.drafter.deck[self.deck_list_box.curselection()[0]]
            self.detail_controller.update_card_display(selected_id)
