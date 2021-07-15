from draft_deck.view.card_choice_frame import CardChoiceFrame
from draft_deck.view.card_detail_frame import CardDetailFrame
from draft_deck.view.deck_list_frame import DeckListFrame
from draft_deck.controller.card_detail_controller import CardDetailController
from draft_deck.model.drafter import Drafter
from draft_deck.model.communication_controller import CommunicationController
import tkinter
from tkinter import ttk
from parameter import IMG_DIR, DB_FILE, POOL_FILE, DECK_DIR, APP_URL
from draft_deck.view.menu_wait_frame import MenuFrame, WaitFrame


def print_hierarchy(w, depth=0):
    print('  ' * depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(
        w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth + 1)


class ChoiceFrame(ttk.Frame):
    def __init__(self, master, drafter, communication_controller):
        super().__init__(master)
        self.master = master
        self.drafter = drafter
        self.communication_controller = communication_controller
        self.card_detail_frame = CardDetailFrame(self, self.drafter, width=200)# why not applied?
        self.card_detail_frame.grid(column=0, row=0)
        self.card_detail_controller = CardDetailController(drafter, self.card_detail_frame)
        self.card_choice_frame = CardChoiceFrame(self, drafter, self.card_detail_controller,self.communication_controller)
        self.card_choice_frame.grid(column=1, row=0)
        self.deck_list_frame = DeckListFrame(self, drafter, self.card_detail_controller)
        self.deck_list_frame.grid(column=2, row=0)


class Application(tkinter.Frame):
    def __init__(self, master, drafter, communication_controller):
        super().__init__(master)
        # root frame config
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        master.geometry("1280x800")
        master.title("online picker")
        # init variables
        self.drafter = drafter
        self.communication_controller = communication_controller
        self.page_move_dict = {"menu": self.menu_scene, "wait": self.wait_scene, "choice": self.choice_scene}
        self.current_frame = MenuFrame(self, lambda: print("menu"))
        self.menu_scene()

    def menu_scene(self):
        """
        move to memu scene
        """
        self.current_frame.destroy()
        self.current_frame = MenuFrame(self, self.communication_controller)
        self.current_frame.grid(column=0, row=0)

    def wait_scene(self):
        """
        move to wait scene
        """
        self.current_frame.destroy()
        self.current_frame = WaitFrame(self, self.communication_controller)
        self.current_frame.grid(column=0, row=0)

    def choice_scene(self):
        """
        move to choice_scene
        """
        self.current_frame.destroy()
        self.current_frame = ChoiceFrame(self, self.drafter, self.communication_controller)
        self.current_frame.grid(column=0, row=0)

    def air_func(self):
        print("air")


def main():
    root = tkinter.Tk()
    drafter = Drafter(IMG_DIR, DB_FILE, POOL_FILE, DECK_DIR)
    communication_controller = CommunicationController(drafter=drafter, app_url=APP_URL)
    app = Application(root, drafter, communication_controller)
    app.mainloop()


if __name__ == "__main__":
    print('Hello')
    main()
