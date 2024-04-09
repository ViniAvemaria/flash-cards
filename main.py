import pandas
from tkinter import *
from random import choice


def random_word():
    try:
        data = pandas.read_csv("./data/words_to_learn.csv")
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        data = pandas.read_csv("./data/french_words.csv")
        data.to_csv("./data/words_to_learn.csv", index=False)
    finally:
        return choice(data.to_dict(orient="records"))


def change_word():
    global current_word, timer
    current_word = random_word()
    root.after_cancel(timer)

    canvas.itemconfig(card_image, image=front_card)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    timer = root.after(3000, change_card, current_word)


def change_card(word):
    canvas.itemconfig(card_image, image=back_card)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word["English"], fill="white")


def remove_word():
    new_data = pandas.read_csv("./data/words_to_learn.csv")
    data_dict = new_data.to_dict(orient="records")
    index = next((i for i, dict in enumerate(data_dict) if dict["French"] == current_word["French"]), None)
    del data_dict[index]
    df = pandas.DataFrame(data_dict)
    df.to_csv("./data/words_to_learn.csv", index=False)
    change_word()


BACKGROUND_COLOR = "#B1DDC6"
current_word = {}

root = Tk()
root.title("Flashy")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = root.after(3000, change_card, current_word)

front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")

# card
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# buttons
right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, border=0, command=remove_word)
right_btn.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, border=0, command=change_word)
wrong_btn.grid(row=1, column=0)

change_word()

root.mainloop()
