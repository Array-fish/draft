# main logic of card_draft
from draft_deck.main import get_card_data
import os
import random
from parse_card_data import parse_card_data,check_extra
import sqlite3
import pandas as pd
from PIL import ImageTk, Image

class Drafter():
    def __init__(self,img_dir,db_file):
        self.deck = list()
        self.packs = list()
        self.img_dir = img_dir
        self.db_file = db_file
        self.cards_var = 0

        con = sqlite3.connect(db_file)
        cur = con.cursor()
        self.datas_df = pd.read_sql("SELECT * FROM datas", con)
        self.texts_df = pd.read_sql("SELECT * FROM texts", con)
        cur.close()
        con.close()
    
    def get_card_data(self,card_id):
        card_df = self.datas_df[self.datas_df["id"]==card_id]
        card_dict = parse_card_data(card_df)
        card_dict["atk"] = card_df["atk"]
        card_dict["def"] = card_df["def"]
        card_dict["level"] = card_df["level"]
        card_dict["text"] = self.texts_df[self.texts_df['id']==card_id]["desc"]
        return card_dict

    def get_card_img(self,card_id):
        img = ImageTk.PhotoImage(Image.open(os.path.join(self.img_dir,card_id)+".jpg"))
        return img
        
    def extra_check(self,card_id):
        card_df = self.datas_df[self.datas_df["id"]==card_id]
        return check_extra(card_df)
    
    def add_deck(self,card_id_list):
        self.deck += card_id_list
        # change deck list
        self.cards_var = self.deck

    def set_cards_var(self,cards_var):
        self.cards_var = cards_var

    def get_new_pack_img(self,pack_cnt):
        new_pack_img = self.packs[pack_cnt * 2:(pack_cnt+1) * 2] # deepcopy?
        return new_pack_img

    def get_new_pack_img(self,pack_cnt):
        new_pack_id = self.packs[pack_cnt * 2:(pack_cnt+1) * 2] # deepcopy?
        return new_pack_id
    


###d
# deck_dict = {"main":list(id),"extra":list(id)}
###
def deck_format(deck_dict,deck_dir):
    os.makedirs(deck_dir, exist_ok=True) 
    deck_name = input("Please input deck name:")
    with open(os.path.join(deck_dir,deck_name+".ydk"),mode="w", encoding="utf-8") as f:
        f.write("#created by ...\n")
        f.write("#main\n")
        f.writelines('\n'.join(deck_dict['main']))
        f.write("\n#extra\n")
        f.writelines('\n'.join(deck_dict['extra']))
        #f.write("\n!side\n")
        #f.writelines('\n'.join(side_id_list))

# monstar:magic:trap:extra:rare = 10:3:3:3:1
# create 4x15x2 packs
def pack_create(card_pool_dict):
    monster_list = random.choices(card_pool_dict["monster"],60)
    magic_list = random.choices(card_pool_dict["magic"],18)
    trap_list = random.choices(card_pool_dict["trap"],18)
    extra_list = random.choices(card_pool_dict["extra"],18)
    rare_list = random.choices(card_pool_dict["rare"],6)
    main_list = monster_list + magic_list + trap_list

    random.shuffle(main_list)
    random.shuffle(extra_list)
    random.shuffle(rare_list)
    packs_list = list()
    for i in range(15):
        if i < 3:
            packs_list.append(main_list[0:4])
            packs_list.append(main_list[4:8])
            del main_list[0:8]
        else:
            if i % 5 == 4:
                for _ in range(2):
                    tmp_list = main_list[0:3]
                    tmp_list.append(rare_list[0])
                    packs_list.append(tmp_list)
                    del main_list[0:3]
                    del rare_list[0]
            else:
                for _ in range(2):
                    tmp_list = main_list[0:3]
                    tmp_list.append(extra_list[0])
                    packs_list.append(tmp_list)
                    del main_list[0:3]
                    del extra_list[0]
    return packs_list

