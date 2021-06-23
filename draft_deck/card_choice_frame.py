#from draft_deck.drafter import Drafter
from tkinter import StringVar, ttk

class Card_Label(ttk.Label):
    def __init__(self,master,bind_func,**arg):
        super().__init__(master,**arg)
        self.id = 0
        self.bind("<ButtonPress-3>",lambda e:bind_func(self.id))

class Pack_display_frame(ttk.Frame):
    def __init__(self,master,detail_controller):
        super().__init__(master)
        self.image_list = list()
        self.id_list = list()
        self.card_label_list = list()
        self.detail_controller = detail_controller

    def set_card_image(self, image_list, id_list):
        self.image_list = image_list
        self.id_list = id_list
        for card_label in self.card_label_list:
            card_label.destroy()
        self.card_label_list = list() # reset list
        #print(image_list)
        for i,aimage in enumerate(self.image_list):
            new_label = Card_Label(self,self.detail_controller.update_card_display,image=aimage)
            new_label.grid(column=i,row=0)
            new_label.columnconfigure(0,weight=1)
            new_label.rowconfigure(0,weight = 1)
            new_label.id = self.id_list[i]
            #new_label.bind("<ButtonPress-3>",lambda e:self.detail_controller.update_card_display(new_label.id))
            self.card_label_list.append(new_label)

class Card_choice_frame(ttk.Frame):
    def __init__(self, master,drafter,detail_controller):
        super().__init__(master)
        self.drafter = drafter
        self.cards_id_upper = list()
        self.cards_id_lower = list()
        self.detail_controller = detail_controller
        # pack progress label
        self.pack_progress = StringVar()
        self.pack_cnt = 1
        self.pack_progress.set(str(self.pack_cnt)+" / 15 pack")
        self.pack_cnt_label = ttk.Label(self,textvariable=self.pack_progress)
        self.pack_cnt_label.grid(column=0,row=0)
        # pack choice radio buttons
        self.which_pack = StringVar()
        self.upper_radio_button = ttk.Radiobutton(self,variable=self.which_pack,value="upper")
        self.lower_radio_button = ttk.Radiobutton(self,variable=self.which_pack,value="under")
        self.upper_radio_button.grid(column=0,row=1)
        self.lower_radio_button.grid(column=0,row=2)

        # pack display frame
        self.pack_display_frame_upper = Pack_display_frame(self,self.detail_controller)
        self.pack_display_frame_upper.grid(column=1,row=1)
        self.pack_display_frame_upper.columnconfigure(0,weight=1)
        self.pack_display_frame_upper.rowconfigure(0,weight=1)

        self.pack_display_frame_lower = Pack_display_frame(self,self.detail_controller)
        self.pack_display_frame_lower.grid(column=1,row=2)
        self.pack_display_frame_lower.columnconfigure(0,weight=1)
        self.pack_display_frame_lower.rowconfigure(0,weight=1)

        new_pack_img_list = self.drafter.get_new_pack_img(self.pack_cnt)
        new_pack_id_list = self.drafter.get_new_pack_id(self.pack_cnt)
        #print(self.drafter,self.pack_cnt,new_pack_id_list)
        #print(new_pack_img_list)
        self.set_pack_img(new_pack_img_list,new_pack_id_list)
        # decide button
        self.pack_choice_button = ttk.Button(self,text = "OK",command=lambda :self.decide_pack())
        self.pack_choice_button.grid(column=0,row=3)

    def set_pack_img(self,pack_img_list,pack_id_list):
        self.cards_id_upper = pack_id_list[0]
        self.cards_id_lower = pack_id_list[1]
        self.pack_display_frame_upper.set_card_image(pack_img_list[0],self.cards_id_upper)
        self.pack_display_frame_lower.set_card_image(pack_img_list[1],self.cards_id_lower)

    def decide_pack(self):
        if self.which_pack.get() == "upper":
            self.drafter.add_deck(self.cards_id_upper)
        else :
            self.drafter.add_deck(self.cards_id_lower)
        if self.pack_cnt == 15:
            self.pack_progress.set("deck creating...")
            self.drafter.create_deck()
        else:
            self.pack_cnt += 1
            new_pack_img_list = self.drafter.get_new_pack_img(self.pack_cnt)
            new_pack_id_list = self.drafter.get_new_pack_id(self.pack_cnt)
            self.set_pack_img(new_pack_img_list,new_pack_id_list)
            self.pack_progress.set(str(self.pack_cnt)+" / 15 pack")

