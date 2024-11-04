from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk 

root = Tk()
root.geometry("300x200")
root.title("Камінь, ножиці, папір")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Глобальні змінні для налаштувань
difficulty = StringVar(value={"Легкий", "Складний"})
mode = StringVar(value={"Класичний", "До 3 перемог", "До 10 перемог"})
player_wins = 0
computer_wins = 0
player_moves = []   # складний режим: тут записуються ходи гравця, які комп'ютер аналізує для виграшного ходу


# Вибір ходу комп'ютера
computer_value = {
    "0": "Камінь",
    "1": "Ножиці",
    "2": "Папір"
}


# Завантаження зображень
rock_img = ImageTk.PhotoImage(Image.open("images/Камінь1.png").resize((120, 120)))
scissors_img = ImageTk.PhotoImage(Image.open("images/Ножниці1.png").resize((120, 120)))
paper_img = ImageTk.PhotoImage(Image.open("images/Папір1.png").resize((120, 120)))

game_window = None
settings_window = None

# Авторство
def info_window():
    info = Toplevel(root)
    info.title('Про нас')
    info.geometry('400x300')
    info.configure(bg='white')
    info_label = Label(info, text="Проект №2.\n Гра \"Камінь, ножиці, папір\"\nАвтори: \nТопольський Олександр\nСкрипник Анастасія\nЯнківська Богдана", font='Arial 14')
    info_label.pack(padx=10, pady=70)

# Налаштування гри
def open_settings_window():
    global settings_window
    settings_window = Toplevel(root)
    settings_window.geometry("300x300")
    settings_window.title("Налаштування гри")

    Label(settings_window, text="Виберіть рівень складності:", font="normal 12 bold").pack(pady=10)
    Radiobutton(settings_window, text="Легкий (Комп'ютер ходить випадковим чином)", variable=difficulty, value="Легкий").pack()
    Radiobutton(settings_window, text="Складний (Комп'ютер аналізує ходи гравця)", variable=difficulty, value="Складний").pack()

    Label(settings_window, text="Виберіть режим гри:", font="normal 12 bold").pack(pady=10)
    Radiobutton(settings_window, text="Класичний", variable=mode, value="Класичний").pack()
    Radiobutton(settings_window, text="До 3 перемог", variable=mode, value="До 3 перемог").pack()
    Radiobutton(settings_window, text="До 10 перемог", variable=mode, value="До 10 перемог").pack()

    Button(settings_window, text="Почати гру", command=lambda: start_game(settings_window)).pack(pady=20)
    if game_window:
        game_window.destroy()

# Запуск гри
def start_game(settings_window):
    root.withdraw()
    if not difficulty.get() or difficulty.get() not in {"Легкий", "Складний"} or \
    not mode.get() or mode.get() not in {"Класичний", "До 3 перемог", "До 10 перемог"}:
        messagebox.showwarning("Увага", "Будь ласка, оберіть і рівень складності, і режим гри.")
        return
    if settings_window:
        settings_window.withdraw()
    open_game_window()
    
# Вікно з грою
def open_game_window():
    global game_window
    game_window = Toplevel(root)
    game_window.geometry("550x650")
    Label(game_window, text="Камінь, ножиці, папір", font="normal 20 bold", fg="blue").pack(pady=20)
    game_window.columnconfigure(0, weight=1)
    game_window.rowconfigure(0, weight=1)
    
    images_frame = Frame(game_window)
    images_frame.pack(pady=10, fill=BOTH, expand=True)

    player_image_label = Label(images_frame)
    player_image_label.pack(side=LEFT, padx=50, expand=True)

    computer_image_label = Label(images_frame)
    computer_image_label.pack(side=RIGHT, padx=50, expand=True)

    global player_wins, computer_wins
    player_wins = 0
    computer_wins = 0

    game_menubar = Menu(game_window)
    game_menubar.add_command(label='Налаштування гри', command=open_settings_window)
    game_menubar.add_command(label='Вихід', command=quit)
    game_window.config(menu=game_menubar)

    # Запис балів
    def update_score():
        score_label.config(text=f"Гравець: {player_wins} - Комп'ютер: {computer_wins}")

    # Режими гри
    def check_winner():
        if mode.get() == "До 3 перемог":
            if player_wins == 3:
                winloselabel.config(text="Гравець виграв матч!")
                disable_buttons()
            elif computer_wins == 3:
                winloselabel.config(text="Комп'ютер виграв матч!")
                disable_buttons()
        
        if mode.get() == "До 10 перемог":
            if player_wins == 10:
                winloselabel.config(text="Гравець виграв матч!")
                disable_buttons()
            elif computer_wins == 10:
                winloselabel.config(text="Комп'ютер виграв матч!")
                disable_buttons()

    def disable_buttons():
        button1["state"] = "disable"
        button2["state"] = "disable"
        button3["state"] = "disable"


    # Перезавантаження гри
    def reset_game():
        global player_wins, computer_wins
        button1["state"] = "active"
        button2["state"] = "active"
        button3["state"] = "active"
        player_image_label.config(image="")
        computer_image_label.config(image="")
        winloselabel.config(text="")
        player_moves.clear()
        player_wins = 0
        computer_wins = 0
        update_score()

    # Як ходить комп'ютер
    def computer_choice(player_choice):
        if difficulty.get() == "Легкий":
            return computer_value[str(random.randint(0, 2))]
        if difficulty.get()=="Складний":
            # Складний рівень: аналізуємо частоту ходів гравця
            if not player_moves:
                return computer_value[str(random.randint(0, 2))]
            move_counts = {"Камінь": 0, "Ножиці": 0, "Папір": 0}
            for move in player_moves:
                move_counts[move] += 1
            # Прогнозуємо найчастіший хід гравця та обираємо контрхід
            predicted_move = max(move_counts, key=move_counts.get)
            if predicted_move == "Камінь":
                return "Папір"
            elif predicted_move == "Ножиці":
                return "Камінь"
            else:
                return "Ножиці"

    # Хід гравця
    def play(player_choice):
        global player_wins, computer_wins
        c_v = computer_choice(player_choice)
        p_v = player_choice
        player_moves.append(player_choice)
        if c_v == p_v:
            match_result = "Нічия"
        elif (player_choice == "Камінь" and c_v == "Ножиці") or \
             (player_choice == "Ножиці" and c_v == "Папір") or \
             (player_choice == "Папір" and c_v == "Камінь"):
            match_result = "Ви виграли!"
            player_wins += 1
        else:
            match_result = "Виграв комп'ютер..." 
            computer_wins += 1
        winloselabel.config(text=match_result)
        label1.config(text=player_choice)
        label3.config(text=c_v)
        update_score()
        check_winner()

        # Показ картинок для ходів комп'ютера та гравця
        if p_v == "Камінь":
            player_image_label.config(image=rock_img)
        elif p_v == "Ножиці":
            player_image_label.config(image=scissors_img)
        elif p_v == "Папір":
            player_image_label.config(image=paper_img)

        if c_v == "Камінь":
            computer_image_label.config(image=rock_img)
        elif c_v == "Ножиці":
            computer_image_label.config(image=scissors_img)
        elif c_v == "Папір":
            computer_image_label.config(image=paper_img)

    # Заголовки, кнопки, рамки
    frame = Frame(game_window)
    frame.pack(expand=True, fill=BOTH)

    frame1 = Frame(game_window)
    frame1.pack(expand=True, fill=BOTH)

    label1 = Label(frame, text="Гравець", font=20, fg="blue")
    label2 = Label(frame, text="VS", font="normal 20 bold")
    label3 = Label(frame, text="Комп'ютер", font=20, fg="red")

    label1.pack(side=LEFT, expand=True, fill=BOTH)
    label2.pack(side=LEFT, expand=True, fill=BOTH)
    label3.pack(side=LEFT, expand=True, fill=BOTH)

    winloselabel = Label(game_window, text="Камінь, ножиці, папір!", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
    winloselabel.pack(pady=20, expand=True, fill=BOTH)

    score_label = Label(game_window, text="Гравець: 0 - Комп'ютер: 0", font="normal 12 bold")
    score_label.pack(pady=10, expand=True, fill=BOTH)

    frame1 = Frame(game_window)
    frame1.pack()

#Ігрові кнопки
    button1 = Button(frame1, text="Камінь", font=10, width=7, command=lambda: play("Камінь"))
    button2 = Button(frame1, text="Папір", font=10, width=7, command=lambda: play("Папір"))
    button3 = Button(frame1, text="Ножиці", font=10, width=7, command=lambda: play("Ножиці"))

    button1.pack(side=LEFT, padx=10, expand=True, fill=BOTH)
    button2.pack(side=LEFT, padx=10, expand=True, fill=BOTH)
    button3.pack(side=LEFT, padx=10, expand=True, fill=BOTH)

    Button(game_window, text="Перезапустити гру", font=20, fg="black", bg="pink", command=reset_game).pack(pady=20, expand=True)

# Головне вікно з кнопкою для початку гри
Label(root, text=" ").pack(pady=5)
Label(root, text="Камінь, ножиці, папір!", font="normal 15 bold", fg="blue").pack(pady=1)
Button(root, text="Почати гру", font=10, command=open_settings_window).pack(pady=5)
Button(root, text="Про нас", font=10, command=info_window).pack(pady=5)

# Запуск проекту
root.mainloop()