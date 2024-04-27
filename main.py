from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
flip_timer = None
flip_timer_active = False
random_word = {}

try:
    data = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    initial_data = pandas.read_csv("./data/french_words.csv")
    data_dict = initial_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

# --------------------Base--------------------:
window = Tk()
window.title("Flashy")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# --------------------Resources--------------------:
right_icon = PhotoImage(file="./images/right.png")
wrong_icon = PhotoImage(file="./images/wrong.png")
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
current_screen = canvas.create_image(400, 263, image=card_front)

# --------------------Labels--------------------:
language_text = canvas.create_text(400, 150, text='French', fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 253, text="word", fill="black", font=("Ariel", 60, "bold"))

# --------------------Functions--------------------:


def randomize_word():
    global flip_timer, flip_timer_active, random_word
    if flip_timer_active:
        window.after_cancel(flip_timer)
    random_word = random.choice(data_dict)
    canvas.itemconfig(current_screen, image=card_front)
    canvas.itemconfig(word_text, text=random_word["French"], fill="black")
    canvas.itemconfig(language_text, text="French", fill="black")
    flip_timer = window.after(3000, flip_card)
    flip_timer_active = True


def flip_card():
    global flip_timer_active
    canvas.itemconfig(current_screen, image=card_back)
    canvas.itemconfig(word_text, text=random_word["English"], fill="white")
    canvas.itemconfig(language_text, text="English", fill="white")
    window.after_cancel(flip_timer)
    flip_timer_active = False


def word_known():
    global random_word
    data_dict.remove(random_word)
    words_to_learn = data_dict
    words_to_learn_data = pandas.DataFrame(words_to_learn)
    words_to_learn_data.to_csv("./data/words_to_learn.csv", index=False)
    randomize_word()


randomize_word()

# --------------------Buttons--------------------:
right_button = Button(image=right_icon, highlightthickness=0, pady=50, bd=0.2, command=word_known)
right_button.grid(column=1, row=1)
wrong_button = Button(image=wrong_icon, highlightthickness=0, pady=50, bd=0.2, command=randomize_word)
wrong_button.grid(column=0, row=1)

window.mainloop()
