from tkinter import StringVar, ttk, N, S, E, W


class CardDetailFrame(ttk.Frame):
    def __init__(self, master, drafter):
        super().__init__(master)
        # variable
        self.display_img = 0
        self.card_detail = StringVar()
        self.drafter = drafter
        # card_label
        self.img_label = ttk.Label(self)
        self.img_label.grid(column=0, row=0, sticky=(N, E, W))
        self.img_label.columnconfigure(0, weight=1)
        self.img_label.rowconfigure(0, weight=1)
        # text_label
        self.detail_label = ttk.Label(self, textvariable=self.card_detail, wraplength=250)
        self.detail_label.grid(column=0, row=1, sticky=(N, S, E, W))
        self.detail_label.columnconfigure(0, weight=1)
        self.detail_label.rowconfigure(0, weight=1)
