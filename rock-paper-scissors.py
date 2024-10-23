from tkinter import *
import random
 
root = Tk()
root.geometry("300x300")
root.title("Гра \"Камінь, ножиці, папір\"")
 
# Хід комп'ютера
computer_value = {
    "0": "Камінь",
    "1": "Ножиці",
    "2": "Папір"
}
 
# Перезапуск гри
def reset_game():
    b1["state"] = "active"
    b2["state"] = "active"
    b3["state"] = "active"
    l1.config(text="Гравець              ")
    l3.config(text="Комп'ютер")
    l4.config(text="")
 
# Деактивація кнопки
def button_disable():
    b1["state"] = "disable"
    b2["state"] = "disable"
    b3["state"] = "disable"
 
# Якщо гравець обрав камінь
def isrock():
    c_v = computer_value[str(random.randint(0, 2))]
    if c_v == "Камінь":
        match_result = "Нічия"
    elif c_v == "Ножиці":
        match_result = "Ви виграли!"
    else:
        match_result = "Виграв комп'ютер..."
    l4.config(text=match_result)
    l1.config(text="Камінь            ")
    l3.config(text=c_v)
    button_disable()
 
# Якщо гравець обрав папір
def ispaper():
    c_v = computer_value[str(random.randint(0, 2))]
    if c_v == "Папір":
        match_result = "Нічия"
    elif c_v == "Ножиці":
        match_result = "Виграв комп'ютер..."
    else:
        match_result = "Ви виграли!"
    l4.config(text=match_result)
    l1.config(text="Папір           ")
    l3.config(text=c_v)
    button_disable()
 
# Якщо гравець обрав ножиці
def isscissor():
    c_v = computer_value[str(random.randint(0, 2))]
    if c_v == "Камінь":
        match_result = "Виграв комп'ютер..."
    elif c_v == "Ножиці":
        match_result = "Нічия"
    else:
        match_result = "Ви виграли!"
    l4.config(text=match_result)
    l1.config(text="Ножиці       ")
    l3.config(text=c_v)
    button_disable()
 
 
# Заголовки, кнопки, рамки
Label(root,
      text="Rock Paper Scissor",
      font="normal 20 bold",
      fg="blue").pack(pady=20)
 
frame = Frame(root)
frame.pack()
 
l1 = Label(frame,
           text="Player  ",
           font=10)
 
l2 = Label(frame,
           text="VS             ",
           font="normal 10 bold")
 
l3 = Label(frame, text="Computer", font=10)
 
l1.pack(side=LEFT)
l2.pack(side=LEFT)
l3.pack()
 
l4 = Label(root,
           text="",
           font="normal 20 bold",
           bg="white",
           width=15,
           borderwidth=2,
           relief="solid")
l4.pack(pady=20)
 
frame1 = Frame(root)
frame1.pack()
 
b1 = Button(frame1, text="Rock",
            font=10, width=7,
            command=isrock)
 
b2 = Button(frame1, text="Paper ",
            font=10, width=7,
            command=ispaper)
 
b3 = Button(frame1, text="Scissor",
            font=10, width=7,
            command=isscissor)
 
b1.pack(side=LEFT, padx=10)
b2.pack(side=LEFT, padx=10)
b3.pack(padx=10)
 
Button(root, text="Reset Game",
       font=10, fg="red",
       bg="black", command=reset_game).pack(pady=20)
 

root.mainloop()