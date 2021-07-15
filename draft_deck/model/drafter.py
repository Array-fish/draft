# main logic of card_draft
import os
import random
from draft_deck.model.parse_card_data import parse_card_data, check_extra
import sqlite3
import pandas as pd
from PIL import ImageTk, Image


class Drafter:
    """
    Draft deck and keep card, user choice.
    manage Data Base and put images and texts.
    """
    def __init__(self, img_dir, db_file, pool_file, deck_dir):
        self.deck = list()
        self.deck_cards_names = list()
        self.img_dir = img_dir
        self.db_file = db_file
        self.pool_file = pool_file
        self.deck_dir = deck_dir
        self.packs = list()
        self.current_pack_id_list = list()
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        self.datas_df = pd.read_sql("SELECT * FROM datas", con)
        self.texts_df = pd.read_sql("SELECT * FROM texts", con)
        cur.close()
        con.close()

    def get_card_data(self, card_id):
        card_df = self.datas_df[self.datas_df["id"] == card_id]
        card_dict = parse_card_data(card_df)
        card_dict["atk"] = card_df["atk"].values
        card_dict["def"] = card_df["def"].values
        card_dict["level"] = card_df["level"].values
        card_dict["text"] = self.texts_df[self.texts_df['id'] == card_id]["desc"].values
        card_dict["name"] = self.texts_df[self.texts_df['id'] == card_id]["name"].values
        return card_dict

    def get_card_img(self, card_id, img_size=(177, 254)):
        img = ImageTk.PhotoImage(Image.open(os.path.join(self.img_dir, str(int(card_id))) + ".jpg").resize(img_size))
        return img

    def _extra_check(self, card_id):
        card_df = self.datas_df[self.datas_df["id"] == card_id]
        return check_extra(card_df)

    def add2deck(self, card_id_list):
        self.deck += card_id_list
        for id in card_id_list:
            self.deck_cards_names.append(self.get_card_data(id)["name"][0])

    def set_current_pack_id(self, pack_id_list):
        self.current_pack_id_list = pack_id_list

    def get_current_pack_img(self):
        pack_img_list = list()
        for card_id in self.current_pack_id_list:
            pack_img_list.append(self.get_card_img(card_id))
        return pack_img_list

    def get_current_pack_id(self):
        return self.current_pack_id_list

    def get_test_pack_id(self):
        return [89943723,89943723,89943723,78371393,64655485,89631139,83764718,23995346,84013237,44508094,99585850,
                53582587,53129443,81439173,581014,5556499,37742478,68860936,28297833]

    def get_test_pack_img(self):
        pack_img_list = list()
        for card_id in [89943723,89943723,89943723,78371393,64655485,89631139,83764718,23995346,84013237,44508094,99585850,
                53582587,53129443,81439173,581014,5556499,37742478,68860936,28297833]:
            pack_img_list.append(self.get_card_img(card_id, (118, 170)))
        return pack_img_list

    def read_card_pool(self):
        pool_df = pd.read_csv(self.pool_file)
        card_pool_dict = dict()
        type_list = ["monster", "magic", "trap", "extra", "rare"]
        for atype in type_list:
            type_df = pool_df[pool_df["type"] == atype]
            card_pool_dict[atype] = list()
            for i in range(len(type_df)):
                card_num = type_df.iloc[i]["num"]
                card_id = type_df.iloc[i]["id"]
                for _ in range(card_num):
                    card_pool_dict[atype].append(card_id)
        return card_pool_dict

    def pack_create(self, card_pool_dict, member_num):
        """
        monstar:magic:trap:extra:rare = 10:3:3:3:1
        create 20x3xmember packs
        """
        monster_list = random.choices(card_pool_dict["monster"], k=30*member_num)
        magic_list = random.choices(card_pool_dict["magic"], k=9*member_num)
        trap_list = random.choices(card_pool_dict["trap"], k=9*member_num)
        extra_list = random.choices(card_pool_dict["extra"], k=9*member_num)
        rare_list = random.choices(card_pool_dict["rare"], k=3*member_num)
        main_list = monster_list + magic_list + trap_list

        random.shuffle(main_list)
        random.shuffle(extra_list)
        random.shuffle(rare_list)
        packs_list = list()
        for p in range(3*member_num):
            apack = monster_list[10*p:10*(p+1)] + magic_list[3*p:3*(p+1)] + trap_list[3*p:3*(p+1)]+extra_list[3*p:3*(p+1)]
            apack.append(rare_list[p])
            packs_list.append(apack)

        return packs_list

    def create_deck(self, deck_name):
        deck_dict = {"main": list(), "extra": list()}
        for id in self.deck:
            if self._extra_check(id):
                deck_dict["extra"].append(str(id))
            else:
                deck_dict["main"].append(str(id))
        deck_format(deck_dict, self.deck_dir, deck_name)


def deck_format(deck_dict, deck_dir, deck_name):
    """
    deck_dict = {"main":list(id),"extra":list(id)}
    """
    os.makedirs(deck_dir, exist_ok=True)
    with open(os.path.join(deck_dir, deck_name + ".ydk"), mode="w", encoding="utf-8") as f:
        f.write("#created by ...\n")
        f.write("#main\n")
        f.writelines('\n'.join(deck_dict['main']))
        f.write("\n#extra\n")
        f.writelines('\n'.join(deck_dict['extra']))
        # f.write("\n!side\n")
        # f.writelines('\n'.join(side_id_list))
