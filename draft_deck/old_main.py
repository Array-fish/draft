# import tkinter
# from tkinter import ttk
# from tkinter import *
# from PIL import ImageTk, Image
# import os
# import pandas as pd
# import random
# import sqlite3
# from parse_card_data import parse_card_data
# import numpy as np
# #from card_display import card_img_frame, display_card_img

# ## parameter please fill in #######################################
# ONE_PICK = 4
# PICKUP_NUM = 60
# POOL_FILE = "..\\cube_pool.csv"
# # fucking global variable ########################################################
# pack_cnt = 1
# packs = np.array([0])
# tmp_card_imgs = list()
# #########################################################

# def chat_desu(df):
#     main_id_list = np.array(rand_main(df),dtype="str")
#     ex_id_list = np.array(rand_ex(df),dtype="str")
#     side_id_list = np.array(rand_side(df),dtype="str")
#     os.makedirs(deck_dir, exist_ok=True) 
#     deck_name = input("Please input deck name:")
#     with open(os.path.join(deck_dir,deck_name+".ydk"),mode="w", encoding="utf-8") as f:
#         f.write("#created by ...\n")
#         f.write("#main\n")
#         f.writelines('\n'.join(main_id_list))
#         f.write("\n#extra\n")
#         f.writelines('\n'.join(ex_id_list))
#         f.write("\n!side\n")
#         f.writelines('\n'.join(side_id_list))

# def load_data():
#     con = sqlite3.connect(DB_FILE)
#     cur = con.cursor()
#     datas_df = pd.read_sql("SELECT * FROM datas", con)
#     texts_df = pd.read_sql("SELECT * FROM texts", con)
#     cur.close()
#     con.close()
#     return datas_df, texts_df

# def create_packs():
#     card_pool = pd.read_csv(POOL_FILE,header=None).values.flatten()
#     #print(card_pool)
#     use_card = random.choices(list(card_pool),k=PICKUP_NUM*2)
#     #use_card = card_pool[use_idx]
#     np.random.shuffle(use_card)
#     packs = np.array(use_card).reshape([int(PICKUP_NUM * 2 / ONE_PICK), ONE_PICK])
#     return packs

# def get_card_data(datas_df,texts_df,id):
#     card_df = datas_df[datas_df["id"]==id]
#     card_dict = parse_card_data(card_df)
#     card_dict["atk"] = card_df["atk"]
#     card_dict["def"] = card_df["def"]
#     card_dict["level"] = card_df["level"]
#     card_dict["text"] = texts_df[texts_df['id']==id]["desc"]
#     return card_dict


# def print_hierarchy(w, depth=0):
#     print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
#     for i in w.winfo_children():
#         print_hierarchy(i, depth+1)

# def print_config(w,depth=0):
#     print("depth",depth)
#     print(w.configure())
#     for i in w.winfo_children():
#         print_config(i,depth+1)

# def display_card_img(img_label,explain_text, card_id,datas_df,texts_df):
#     print("display card image")
#     card_img = ImageTk.PhotoImage(Image.open(os.path.join(PICS_DIR,card_id)+".jpg"))
#     img_label.configure(img=card_img)
#     card_data_dict = get_card_data(datas_df, texts_df, id)
#     tmp_explain_text = "["
#     for type in card_data_dict["type"]:
#         tmp_explain_text = tmp_explain_text + type + "|"
#     tmp_explain_text += "]"
#     tmp_explain_text += card_data_dict["race"]+"/"+card_data_dict["attribute"]+"\n"
#     tmp_explain_text += "[★"+card_data_dict["level"]+"]"+card_data_dict["atk"]+"/"+card_data_dict["def"]+"\n"
#     tmp_explain_text += card_data_dict["text"]
#     explain_text.set(tmp_explain_text)# get_text()

# def get_img(id):
#     # print("get_img")
#     return ImageTk.PhotoImage(Image.open(os.path.join(PICS_DIR,str(id)+".jpg")).resize((177,254)))

# def choice_pack(*args,which_pack,current_pack_display,lb,up_low_s,items):
#     global pack_cnt
#     global packs
#     global tmp_card_imgs
#     insert_cards = list()
#     print(which_pack.get())
#     if which_pack.get() == "upper":
#         insert_cards = packs[0]
#     else:
#         insert_cards = packs[1]
    
#     print(items.get(),type(items.get()))
#     items_list = items.get()
#     items_list = items_list.replace("'","").replace('(','').replace(')','')
#     items_list = items_list.split(', ')
#     for card_id in insert_cards:
#         #lb.insert(card_id)
#         #print(lb.configure())
#         items_list.append(card_id)
#     items.set(items_list)
#     lb.configure(listvariable = items)
#     #print(packs)
#     packs = np.delete(packs,[0,1],0)
#     #print(packs)
#     pack_cnt+=1
#     current_pack_display.set(str(pack_cnt)+" / 15 pack")
#     if(pack_cnt == 15):
#         create_deck(lb)
#     else:
#         for i in range(4):
#             tmp_card_imgs[0][i] = get_img(packs[0][i])
#             tmp_card_imgs[1][i] = get_img(packs[1][i])
#             up_low_s[0][i].configure(image = tmp_card_imgs[0][i])
#             up_low_s[1][i].configure(image = tmp_card_imgs[1][i])



# # def card_img_frame(frame):
# #     img_label = ttk.Label(frame,borderwidth=5, relief="ridge")
# #     explain_label = ttk.Label(frame,borderwidth=5, relief="ridge")
# #     explain_text = StringVar()
# #     explain_label["textvariable"] = explain_text
# #     explain_text.set("initial text")
# #     initial_img = ImageTk.PhotoImage(Image.open("..\\pics\\10000.jpg"))
# #     img_label['image'] = initial_img
# #     img_label.grid(column=0, row=0, sticky=(E, W))
# #     explain_label.grid(column=0,row=1, sticky=(E, W))
# #     img_label.columnconfigure(0, weight=1)
# #     img_label.rowconfigure(0, weight=1)
# #     explain_label.columnconfigure(0, weight=1)
# #     explain_label.rowconfigure(0, weight=1)
    
# #     display_card_img(label,"..\\pics\\10000.jpg")


# def main():
#     # business logic ----------------------------------
#     datas_df, texts_df = load_data()
#     global packs
#     global pack_cnt
#     packs = create_packs()
#     pack_cnt = 1
#     # view -------------------------------------------
#     # root
#     root = tkinter.Tk()
#     root.geometry('1280x720')
#     root.columnconfigure(0, weight=1)
#     root.rowconfigure(0, weight=1)
#     # content frame
#     content = ttk.Frame(root)
#     content.grid(column=0, row=0, sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
#     content.columnconfigure(0, weight=1)
#     content.rowconfigure(0, weight=1)
#     # card_frame #######################################
#     card_frame = ttk.Frame(content, borderwidth=5, relief="ridge")
#     card_frame.grid(column=0, row=0,sticky=(tkinter.N,tkinter.S,tkinter.W))
#     card_frame.columnconfigure(0, weight=1)
#     card_frame.rowconfigure(0, weight=1)
#     # image_label
#     img_label = ttk.Label(card_frame,borderwidth=5, relief="ridge")
#     #initial_img = ImageTk.PhotoImage(Image.open("..\\pics\\10000.jpg"))
#     initial_img = get_img(10000)
#     img_label['image'] = initial_img
#     img_label.grid(column=0, row=0, sticky=(E, W))
#     img_label.columnconfigure(0, weight=1)
#     img_label.rowconfigure(0, weight=1)
#     # explain label
#     explain_label = ttk.Label(card_frame,borderwidth=5, relief="ridge")
#     explain_text = StringVar()
#     explain_label["textvariable"] = explain_text
#     explain_text.set("initial text")
#     explain_label.grid(column=0,row=1, sticky=(E, W))
#     explain_label.columnconfigure(0, weight=1)
#     explain_label.rowconfigure(0, weight=1)
#     # list frame ####################################################
#     list_frame = ttk.Frame(content,borderwidth=5, relief="ridge")
#     list_frame.grid(column=2, row=0,sticky=(tkinter.N,tkinter.S,tkinter.E))
#     list_frame.columnconfigure(0, weight=1)
#     list_frame.rowconfigure(0, weight=1)
#     # scrallbar
#     items = StringVar()
#     #items.set(["air_id"])
#     lb = Listbox(list_frame, listvariable = items, height=10)
#     lb.grid(column=0, row=0, sticky=(N,W,E,S))
#     s = ttk.Scrollbar(list_frame, orient=VERTICAL, command=lb.yview)
#     s.grid(column=1, row=0, sticky=(N,S))
#     lb['yscrollcommand'] = s.set
#     # select frame ##############################################
#     select_frame = ttk.Frame(content,borderwidth=5, relief="ridge")
#     select_frame.grid(column=1, row=0,sticky=(tkinter.N,tkinter.S,tkinter.W,tkinter.E))
#     select_frame.columnconfigure(0, weight=1)
#     select_frame.rowconfigure(0, weight=1)
#     # current packs label
#     current_pack_display = StringVar()
#     current_pack = ttk.Label(select_frame)
#     current_pack["textvariable"] = current_pack_display
#     current_pack_display.set("1 / 15 pack")
#     current_pack.grid(column=0,row=0)
#     # radio botton
#     which_pick = StringVar()
#     upper = ttk.Radiobutton(select_frame,variable=which_pick,value="upper")
#     lower = ttk.Radiobutton(select_frame,variable=which_pick,value="lower")
#     upper.grid(column=0,row=1)
#     upper.columnconfigure(0, weight=1)
#     upper.rowconfigure(0, weight=1)
#     lower.grid(column=0,row=2)
#     lower.columnconfigure(0, weight=1)
#     lower.rowconfigure(0, weight=1)
#     # upper candicate label
#     u1 = ttk.Label(select_frame)
#     u2 = ttk.Label(select_frame)
#     u3 = ttk.Label(select_frame)
#     u4 = ttk.Label(select_frame)
#     global tmp_card_imgs
#     for ul in range(2):
#         ul_list =list()
#         for i in range(4):
#             ul_list.append(get_img(packs[ul][i]))
#         tmp_card_imgs.append(ul_list)
#     u1['image'] = tmp_card_imgs[0][0]
#     u2['image'] = tmp_card_imgs[0][1]
#     u3['image'] = tmp_card_imgs[0][2]
#     u4['image'] = tmp_card_imgs[0][3]
#     u1.grid(column=1, row=1)
#     u2.grid(column=2, row=1)
#     u3.grid(column=3, row=1)
#     u4.grid(column=4, row=1)
#     #u1.bind("<Button-3>",lambda e: u1.configure(image=get_img(packs[0][0])))
#     # lower candidate label
#     l1 = ttk.Label(select_frame)
#     l2 = ttk.Label(select_frame)
#     l3 = ttk.Label(select_frame)
#     l4 = ttk.Label(select_frame)
#     l1['image'] = tmp_card_imgs[1][0]
#     l2['image'] = tmp_card_imgs[1][1]
#     l3['image'] = tmp_card_imgs[1][2]
#     l4['image'] = tmp_card_imgs[1][3]
#     l1.grid(column=1, row=2)
#     l2.grid(column=2, row=2)
#     l3.grid(column=3, row=2)
#     l4.grid(column=4, row=2)
#     # dicide button
#     up_low_s = [
#         [u1,u2,u3,u4],
#         [l1,l2,l3,l4]
#     ]
#     deside_button = ttk.Button(select_frame,text="OK",command = lambda: choice_pack(which_pack = which_pick,current_pack_display=current_pack_display,lb=lb,up_low_s=up_low_s,items = items))
#     deside_button.grid(column=0,row=3)
#     # # list frame ####################################################
#     # list_frame = ttk.Frame(content,borderwidth=5, relief="ridge")
#     # list_frame.grid(column=2, row=0,sticky=(tkinter.N,tkinter.S,tkinter.E))
#     # list_frame.columnconfigure(0, weight=1)
#     # list_frame.rowconfigure(0, weight=1)
#     # # scrallbar
#     # lb = Listbox(list_frame, height=10)
#     # lb.grid(column=0, row=0, sticky=(N,W,E,S))
#     # s = ttk.Scrollbar(list_frame, orient=VERTICAL, command=l.yview)
#     # s.grid(column=1, row=0, sticky=(N,S))
#     # lb['yscrollcommand'] = s.set
#     ##############################################################
#     root.grid_columnconfigure(0, weight=1)
#     root.grid_rowconfigure(0, weight=1)

#     root.mainloop()


# if __name__ == "__main__":
#     main()