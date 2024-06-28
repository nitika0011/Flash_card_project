from tkinter import *
import pandas
import csv
import random

#---------------------------------Constants----------------------------------------#

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
#-----------------------------------reading the files------------------------------#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
# data_dict = {row.French:row.English for (index,row) in data.iterrows()}
# # french_dataframe = pandas.DataFrame(data)
# french_flash = input(random.choice(data_dict))

# print(to_learn)


#------------------------------------creating functions----------------------------#
def next_card():    
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # print(current_card["French"])
    canvas.itemconfig(card_title, text="French",fill="black")
    canvas.itemconfig(card_word, text=current_card["French"],fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer =window.after(3000, func=flip_card)
    
def flip_card():
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
    # window.after(3000,func=flip_card)
    # print(current_card["English"])

def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
#------------------------------------UI Setup---------------------------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
flip_timer=window.after(3000, func=flip_card)


canvas = Canvas(width=800,height=526)
# my_img =  PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
# button = Button(image=front_img,highlightthickness=0)
card_background = canvas.create_image(400,263,image=card_front_img,)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400,150,text="Title", font=("Ariel", 35, "italic"))
card_word = canvas.create_text(400,263,text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0,row=0,columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, command=flip_card)
unknown_button.grid(column=0,row=1)
check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img,command=is_known)
known_button.grid(column=1, row=1)

next_card()
 
window.mainloop()