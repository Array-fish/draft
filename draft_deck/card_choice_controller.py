import requests


class CardChoiceController:
    def __init__(self, drafter, card_choice_frame):
        self.drafter = drafter
        self.choice_frame = card_choice_frame

    def fetch_cards_id(self):
        id_list = requests.get()
        img_list = self.drafter.get_new_pack_img(id_list)
        self.card_choice_frame.set_pack_img(id_list, img_list)
