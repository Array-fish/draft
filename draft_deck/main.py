from draft_deck.card_detail_frame import card_detail_frame
from card_choice_frame import Card_choice_frame
from card_detail_frame import Card_detail_frame
from deck_list_frame import Deck_list_frame
from drafter import Drafter
import tkinter
from tkinter import ttk

###############################
IMG_DIR = ""
DB_FILE = ""
################################

def main():
    root = tkinter.Tk()
    root.geometry("1280x720")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    drafter = Drafter(IMG_DIR,DB_FILE)
    card_detail_frame = Card_detail_frame(root,drafter)
    card_choice_frame = Card_choice_frame(root,drafter)
    deck_list_frame = Deck_list_frame(root,drafter)

    root.mainloop()



if __name__ == "__main__":
    main()
