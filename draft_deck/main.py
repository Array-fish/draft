from card_choice_frame import CardChoiceFrame
from card_detail_frame import CardDetailFrame
from deck_list_frame import DeckListFrame
from card_detail_controller import Card_detail_controller
from drafter import Drafter
import tkinter
from parameter import IMG_DIR, DB_FILE, POOL_FILE, DECK_DIR
from communication_controller import CommunicationController

def print_hierarchy(w, depth=0):
    print('  ' * depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(
        w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth + 1)


def main():
    root = tkinter.Tk()
    root.geometry("1280x720")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    drafter = Drafter(IMG_DIR, DB_FILE, POOL_FILE, DECK_DIR)
    communication_controller = CommunicationController(drafter=drafter)
    drafter.start()
    card_detail_frame = CardDetailFrame(root, drafter)
    card_detail_frame.grid(column=0, row=0)
    card_detail_controller = Card_detail_controller(drafter, card_detail_frame)
    card_choice_frame = CardChoiceFrame(root, drafter, card_detail_controller)
    card_choice_frame.grid(column=1, row=0)
    deck_list_frame = DeckListFrame(root, drafter, card_detail_controller)
    deck_list_frame.grid(column=2, row=0)

    # print_hierarchy(root)
    root.mainloop()


if __name__ == "__main__":
    print('Hello')
    main()
