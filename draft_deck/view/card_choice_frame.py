from tkinter import StringVar, ttk, N, S, W, E


class NameFormFrame(ttk.Frame):
    def __init__(self, master, drafter):
        super().__init__(master)
        self.drafter = drafter
        self.text = ttk.Label(self, text="Please fill in deck name:").grid(column=0, row=0)
        self.name_value = StringVar()
        self.name_form = ttk.Entry(self, textvariable=self.name_value).grid(column=0, row=1)
        self.button = ttk.Button(self, text="OK", command=self.create_deck).grid(column=0, row=2)

    def create_deck(self):
        deck_name = self.name_value.get()
        if deck_name == "":
            return
        else:
            self.drafter.create_deck(deck_name)
            self.master.destroy()


class CardLabel(ttk.Label):
    ''' ttk.Label for Card img. This have id and fuction fired by left click.'''

    def __init__(self, master, left_callback, right_callback, idx, id, **arg):
        super().__init__(master, **arg)
        self.idx = idx
        self.id = id
        self.bind("<ButtonPress-1>", lambda e: left_callback(self.idx))
        self.bind("<ButtonPress-3>", lambda e: right_callback(self.id))


class PackDisplayFrame(ttk.Frame):
    def __init__(self, master, detail_callback):
        super().__init__(master)
        self.image_list = list()
        self.id_list = list()
        self.card_label_list = list()
        self.detail_callback = detail_callback
        self.selected_id = None
        self._prev_selected_idx = None
        self.card_per_line = 5 # const parameter

    def set_card_image(self, image_list, id_list):
        self.image_list = image_list
        self.id_list = id_list

        # destroy old label
        for card_label in self.card_label_list:
            card_label.destroy()
        self.card_label_list = list()  # reset list
        # create new label
        for idx, (id, img) in enumerate(zip(self.id_list, self.image_list)):
            new_label = CardLabel(self, right_callback=self.detail_callback, left_callback=self.choice_card, idx=idx, id=id, image=img,background="black")
            new_label.grid(column=idx % self.card_per_line, row=int(idx/self.card_per_line),padx=3,pady=3)
            new_label.columnconfigure(0, weight=1)
            new_label.rowconfigure(0, weight=1)
            self.card_label_list.append(new_label)

    def choice_card(self, selected_idx):
        # change label color
        if self._prev_selected_idx is not None:
            self.card_label_list[self._prev_selected_idx].configure(background="black")
        self.card_label_list[selected_idx].configure(background="red")
        self._prev_selected_idx = selected_idx
        self.selected_id = self.id_list[selected_idx]


class CardChoiceFrame(ttk.Frame):
    def __init__(self, master, drafter, card_detail_controller, communication_controller):
        super().__init__(master)
        self.drafter = drafter
        self.cards_id = list()
        self.card_detail_callback = card_detail_controller.update_card_display
        self.communication_controller = communication_controller
        self.selected_id = None
        # reload button
        self.reload_button = ttk.Button(self, text="reload", command=self.reload_frame)
        self.reload_button.grid(column=0, row=0)
        # pack progress label
        self.pack_progress = StringVar()
        self.pack_cnt = 1
        self.pack_progress.set(str(self.pack_cnt) + " / 6 pack")
        self.pack_cnt_label = ttk.Label(self, textvariable=self.pack_progress)
        self.pack_cnt_label.grid(column=1, row=0)
        # pick player label
        self.pick_player = StringVar()
        self.pick_player_frame = ttk.Label(self, textvariable=self.pick_player)
        self.pick_player_frame.grid(column=0, row=1)
        # pack display frame
        self.pack_display_frame = PackDisplayFrame(self, self.card_detail_callback)
        self.pack_display_frame.grid(column=0, row=2)
        self.pack_display_frame.columnconfigure(0, weight=1)
        self.pack_display_frame.rowconfigure(0, weight=1)
        self.card_detail_callback(10000)
        # decide button
        self.pack_choice_button = ttk.Button(self, text="OK", command=self.decide_card)
        self.pack_choice_button.grid(column=0, row=3)
        ## init function
        self.reload_frame()
        # init_pack_img_list = self.drafter.get_current_pack_img()
        # init_pack_id_list = self.drafter.get_current_pack_id()
        init_pack_img_list = self.drafter.get_test_pack_img()
        init_pack_id_list = self.drafter.get_test_pack_id()
        self.set_pack_img(init_pack_img_list, init_pack_id_list)
        if self.communication_controller.is_my_turn():
            self.pack_choice_button.state(["!disabled"])
        else:
            self.pack_choice_button.state(["disabled"])

    def set_pack_img(self, pack_img_list, pack_id_list):
        self.cards_id = pack_id_list
        self.pack_display_frame.set_card_image(pack_img_list, self.cards_id)

    def decide_card(self):
        # not selected
        if self.pack_display_frame.selected_id is None:
            return

        self.selected_id = self.pack_display_frame.selected_id
        #print(self.selected_id)
        self.pack_display_frame.selected_id = None

        self.communication_controller.pick_card(self.selected_id)
        id_list = self.drafter.get_current_pack_id()
        img_list = self.drafter.get_current_pack_img()
        if len(id_list) == 0:
            self.choice_frame.pack_progress.set("deck creating...")
            self.create_name_form_frame()
        else:
            self.pack_progress.set(str(self.pack_cnt) + " / 6 pack")
            self.pick_player.set(self.communication_controller.get_turn_player())
            self.set_pack_img(img_list, id_list)
            if self.communication_controller.is_my_turn():
                self.pack_choice_button.state(['!disabled'])
            else:
                self.pack_choice_button.state(['disabled'])

    def reload_frame(self):
        self.communication_controller.reload_pack()
        self.pick_player.set(self.communication_controller.get_turn_player())
        current_pack_img_list = self.drafter.get_current_pack_img()
        current_pack_id_list = self.drafter.get_current_pack_id()
        self.set_pack_img(current_pack_img_list, current_pack_id_list)
        if self.communication_controller.is_my_turn():
            self.pack_choice_button.state(["!disabled"])
        else:
            self.pack_choice_button.state(["disabled"])
