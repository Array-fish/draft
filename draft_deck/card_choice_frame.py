#from draft_deck.drafter import Drafter
from tkinter import StringVar, ttk

class Pack_display_frame(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        #self.card_label_list = list()
        self.image_list = list()

    def set_card_image(self, image_list):
        self.image_list = image_list
        for card_label in self.card_label_list:
            card_label.destroy()

        for i,aimage in enumerate(image_list):
            new_label = ttk.Label(self.master,image=aimage)
            new_label.gird(colmun=i,row=0)
            new_label.columnconfigure(0,weight=1)
            new_label.rowconfigure(0,weight = 1)
            self.card_label_list.append(new_label)

class Card_choice_frame(ttk.Frame):
    def __init__(self, master,drafter):
        super().__init__(master)
        self.drafter = drafter
        self.cards_id_upper = list()
        self.cards_id_lower = list()
        # pack progress label
        self.pack_progress = StringVar()
        self.pack_cnt = 1
        self.pack_progress.set(int(self.pack_cnt)+" / 15 pack")
        self.pack_cnt_label = ttk.Label(master,textvariable=self.pack_progress)
        self.pack_cnt_label.grid(column=0,row=0)
        # pack choice radio buttons
        self.which_pack = StringVar()
        self.upper_radio_button = ttk.Radiobutton(master,variable=self.which_pack,value="upper")
        self.lower_radio_button = ttk.Radiobutton(master,variable=self.which_pack,value="under")
        self.upper_radio_button.grid(column=0,row=1)
        self.lower_radio_button.grid(column=0,row=2)

        # pack display frame
        self.pack_display_frame_upper = Pack_display_frame(master)
        self.pack_display_frame_upper.grid(column=1,row=1)
        self.pack_display_frame_upper.columnconfigure(0,weight=1)
        self.pack_display_frame_upper.rowconfigure(0,weight=1)

        self.pack_display_frame_lower = Pack_display_frame(master)
        self.pack_display_frame_lower.grid(column=1,row=1)
        self.pack_display_frame_lower.columnconfigure(0,weight=1)
        self.pack_display_frame_lower.rowconfigure(0,weight=1)

        new_pack_img_list = self.drafter.get_new_pack_img()
        new_pack_id_list = self.drafter.get_new_pack_id()
        self.set_pack_img(new_pack_img_list,new_pack_id_list)
        # decide button
        self.pack_choice_button = ttk.Button(master,text = "OK",command=lambda:(self.decide_pack()))

    def set_pack_img(self,pack_img_list,pack_id_list):
        self.cards_id_upper = pack_id_list[0]
        self.cards_id_lower = pack_id_list[1]
        self.pack_display_frame_upper.set_card_image(pack_img_list[0])
        self.pack_display_frame_lower.set_card_image(pack_img_list[1])

    def decide_pack(self):
        if self.which_pack.get() == "upper":
            self.drafter.add_deck(self.cards_id_upper)
        else :
            self.drafter.add_deck(self.cards_id_lower)
        new_pack_img_list = self.drafter.get_new_pack_img()
        new_pack_id_list = self.drafter.get_new_pack_id()
        self.set_pack_img(new_pack_img_list,new_pack_id_list)
        self.pack_cnt += 1
        self.pack_progress.set(int(self.pack_cnt)+" / 15 pack")

