from tkinter import ttk, StringVar


class MenuFrame(ttk.Frame):
    def __init__(self, master, communication_controller):
        super().__init__(master)
        self.master = master
        self.communication_controller = communication_controller
        # player name label
        self.player_name_label = ttk.Label(self, text="player name:")
        self.player_name_label.grid(column=0, row=0)
        # player name entry
        self.player_name = StringVar()
        self.player_name_entry = ttk.Entry(self, textvariable=self.player_name)
        self.player_name_entry.grid(column=1, row=0)
        # room pass label
        self.room_key_label = ttk.Label(self, text="room pass:")
        self.room_key_label.grid(column=0, row=1)
        # room pass entry
        self.room_pass = StringVar()
        self.room_pass_entry = ttk.Entry(self, textvariable=self.room_pass)
        self.room_pass_entry.grid(column=1, row=1)

        # join room button
        self.join_room_button = ttk.Button(self, text="join", command=self.join_or_create_room)
        self.join_room_button.grid(column=0, row=2)

    def join_or_create_room(self):
        #self.communication_controller.create_or_entry_room(self.room_pass.get(), self.player_name.get())
        self.master.page_move_dict["wait"]()


class WaitFrame(ttk.Frame):
    def __init__(self, master, communication_controller):
        super().__init__(master)
        self.master = master
        self.communication_controller = communication_controller
        # back button
        self.back_button = ttk.Button(self, text="back", command=self.delete_room_back_menu)
        self.back_button.grid(column=0, row=0)
        # reload button
        self.reload_button = ttk.Button(self, text="reload", command=self.check_room_go_choice)
        self.reload_button.grid(column=0, row=1)
        # player label
        self.player = StringVar()
        self.player_label = ttk.Label(self, textvariable=self.player)
        self.player_label.grid(column=0, row=2)
        # init func
        self.check_room_go_choice()

    def delete_room_back_menu(self):
        # if anthoer player is ready go to choice
        if self.check_room_go_choice():
            return
        self.communication_controller.delete_room()
        self.master.page_move_dict["menu"]()

    def check_room_go_choice(self):
        #all_ready, player_names = self.communication_controller.check_room_status()
        all_ready, player_names = True, ["hide","aoyama"]
        player_label_content = ""
        for name in player_names:
            player_label_content += name + "\n"
        self.player.set(player_label_content)
        if all_ready:
            self.master.page_move_dict["choice"]()
            return True
