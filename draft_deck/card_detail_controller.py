class Card_detail_controller:
    def __init__(self,drafter,card_detail_frame):
        self.drafter = drafter
        self.card_detail_frame = card_detail_frame

    def display_card(self,img):
        self.card_detail_frame.display_img = img
        self.card_detail_frame.img_label.configure(image = self.card_detail_frame.display_img)

    def set_card_detail(self,card_data_dict):
        #print(card_data_dict)
        tmp_explain_text = card_data_dict["name"][0]+"\n" 
        tmp_explain_text += "["
        for type in card_data_dict["type"]:
            tmp_explain_text = tmp_explain_text + type + "|"
        tmp_explain_text += "]"
        if card_data_dict["race"]:
            tmp_explain_text += card_data_dict["race"][0]+"/"+card_data_dict["attribute"][0]+"\n"
            tmp_explain_text += "[★"+str(card_data_dict["level"][0])+"]"+str(card_data_dict["atk"][0])+"/"+str(card_data_dict["def"][0])
        tmp_explain_text += "\n"
        if card_data_dict["setcode"]:
            tmp_explain_text += "カテゴリー: "
            for category in card_data_dict["setcode"]:
                tmp_explain_text += category + " / "
            tmp_explain_text += "\n"
        tmp_explain_text += card_data_dict["text"][0]
        self.card_detail_frame.card_detail.set(tmp_explain_text)

    def update_card_display(self,card_id):
        self.display_card(self.drafter.get_card_img(card_id))
        card_dict = self.drafter.get_card_data(card_id)
        self.set_card_detail(card_dict)
