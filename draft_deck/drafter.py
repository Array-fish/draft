# main logic of card_draft
import os
import random
from parse_card_data import parse_card_data,check_extra
import sqlite3
import pandas as pd
from PIL import ImageTk, Image
import math
import numpy as np

class Drafter():
    def __init__(self,img_dir,db_file,pool_file,deck_dir):
        self.deck = list()
        self.deck_name = list()
        self.img_dir = img_dir
        self.db_file = db_file
        self.pool_file = pool_file
        self.deck_dir = deck_dir
        self.cards_var = 0
        self.packs = self.pack_create(self.read_card_pool()) 
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        self.datas_df = pd.read_sql("SELECT * FROM datas", con)
        self.texts_df = pd.read_sql("SELECT * FROM texts", con)
        cur.close()
        con.close()
    
    def get_card_data(self,card_id):
        card_df = self.datas_df[self.datas_df["id"]==card_id]
        card_dict = parse_card_data(card_df)
        card_dict["atk"] = card_df["atk"].values
        card_dict["def"] = card_df["def"].values
        card_dict["level"] = card_df["level"].values
        card_dict["text"] = self.texts_df[self.texts_df['id']==card_id]["desc"].values
        card_dict["name"] = self.texts_df[self.texts_df['id']==card_id]["name"].values
        return card_dict

    def get_card_img(self,card_id):
        img = ImageTk.PhotoImage(Image.open(os.path.join(self.img_dir,str(int(card_id)))+".jpg").resize((177,254)))
        return img
        
    def extra_check(self,card_id):
        card_df = self.datas_df[self.datas_df["id"]==card_id]
        return check_extra(card_df)
    
    def add_deck(self,card_id_list):
        self.deck += card_id_list
        for id in card_id_list:
            self.deck_name.append(self.get_card_data(id)["name"][0])
        # change deck list
        self.cards_var.set(self.deck_name)

    def set_cards_var(self,cards_var):
        self.cards_var = cards_var

    def get_new_pack_img(self,pack_cnt):
        new_pack_id = self.get_new_pack_id(pack_cnt)
        new_pack_img = list()
        for pack_id in new_pack_id:
            tmp_pack_img =list()
            for id in pack_id:
                tmp_pack_img.append(self.get_card_img(id))
            new_pack_img.append(tmp_pack_img)
        return new_pack_img

    # pack_cnt is 1-index
    def get_new_pack_id(self,pack_cnt):
        new_pack_id = self.packs[(pack_cnt-1) * 2:pack_cnt * 2]
        return new_pack_id
    
    def read_card_pool(self):
        pool_df = pd.read_csv(self.pool_file)
        card_pool_dict = dict()
        type_list = ["monstar","magic","trap","extra","rare"]
        for atype in type_list:
            card_pool_dict[atype] = list(pool_df[atype])
            for idx,id in enumerate(card_pool_dict[atype]):
                if math.isnan(id):
                    #print(idx,id)
                    card_pool_dict[atype] = np.array(card_pool_dict[atype][0:idx]).astype('int')
                    break
        return card_pool_dict

    # monstar:magic:trap:extra:rare = 10:3:3:3:1
    # create 4x15x2 packs
    def pack_create(self, card_pool_dict):
        monster_list = random.choices(card_pool_dict["monstar"],k=60)
        magic_list = random.choices(card_pool_dict["magic"],k=18)
        trap_list = random.choices(card_pool_dict["trap"],k=18)
        extra_list = random.choices(card_pool_dict["extra"],k=18)
        rare_list = random.choices(card_pool_dict["rare"],k=6)
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

    def create_deck(self,deck_name):
        deck_dict = {"main":list(), "extra":list()}
        for id in self.deck:
            if self.extra_check(id):
                deck_dict["extra"].append(str(id))
            else :
                deck_dict["main"].append(str(id))
        deck_format(deck_dict,self.deck_dir,deck_name)
###d
# deck_dict = {"main":list(id),"extra":list(id)}
###
def deck_format(deck_dict,deck_dir,deck_name):
    #print(deck_dict)
    os.makedirs(deck_dir, exist_ok=True) 
    with open(os.path.join(deck_dir,deck_name+".ydk"),mode="w", encoding="utf-8") as f:
        f.write("#created by ...\n")
        f.write("#main\n")
        f.writelines('\n'.join(deck_dict['main']))
        f.write("\n#extra\n")
        f.writelines('\n'.join(deck_dict['extra']))
        #f.write("\n!side\n")
        #f.writelines('\n'.join(side_id_list))



