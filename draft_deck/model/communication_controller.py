import requests


class CommunicationController:
    def __init__(self, drafter, app_url):
        self.drafter = drafter
        self.url = app_url
        self.room_key = ""
        self.room_pass = ""
        self.player_name = ""
        self.players_list = list()
        self.player_id = 0
        self.turn_player_idx = 0
        self._is_my_turn = False

    def pick_card(self, card_id):
        self.drafter.add2deck([card_id])
        item_data = {"room_key": self.room_key, "card_id": card_id}
        r = requests.post("{}/{}/{}/".format(self.url, self.room_pass, self.player_id), json=item_data)
        json_r = r.json()
        current_pack_id_list, self.turn_player_idx = json_r["pack_id"], json_r["turn_player_idx"]
        self.drafter.set_current_pack_id(current_pack_id_list)
        if self.turn_player_idx == self.player_id:
            self._is_my_turn = True
        else:
            self._is_my_turn = False

        return current_pack_id_list

    def create_or_entry_room(self, room_pass, player_name, player_num=0):
        if room_pass.strip() == "" or player_name.strip() == "":
            return
        self.room_pass = room_pass.strip()
        self.player_name = player_name.strip()
        # if room is exist?
        item_data ={
            "player_name": player_name
        }
        r = requests.get(self.url+"/room/{}".format(room_pass))
        json_data = r.json()
        if json_data["status"] == "waiting":
            # enter room
            er = requests.put(self.url + "/room/{}".format(room_pass), json=item_data)
            json_er = er.json()
            self.player_id, self.room_key = json_er["player_id"], json_er["room_key"]
            self.room_pass = room_pass
        elif json_data["status"] == "not exist":
            # create room
            # item_data["player_num"] = player_num TODO:implement later
            packs = self.drafter.pack_create(self.drafter.read_card_pool())
            item_data["packs"] = packs
            cr = requests.post("{}/room/{}".format(self.url, room_pass))
            json_cr = cr.json()
            self.player_id, self.room_key = json_cr["player_id"], json_cr["room_key"]
            self.room_pass = room_pass
        elif json_data["status"] == "working":
            print("This room pass is already used!!!!!")
            return

    def check_room_status(self):
        # TODO implement.
        all_ready = False
        player_names = list()
        r = requests.get("{}/room/{}".format(self.url, self.room_pass))
        json_r = r.json()
        self.players_list = json_r["players_list"]
        if len(self.players_list) == 2: # TODO: adopt to multi player
            all_ready = True
        return all_ready, self.players_list

    def reload_pack(self):
        r = requests.get("{}/{}/{}/".format(self.url, self.room_pass, self.player_id))
        json_r = r.json()
        current_pack_id_list, turn_player = json_r["pack_id"], json_r["turn_player"]
        self.drafter.set_current_pack_id(current_pack_id_list)
        if turn_player == self.player_id:
            self._is_my_turn = True
        else:
            self._is_my_turn = False

        return current_pack_id_list

    def is_my_turn(self):
        return self._is_my_turn

    def get_turn_player(self):
        return self.players_list[self.turn_player_idx]
