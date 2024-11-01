from tkinter import *
import random

root = Tk()
root.geometry("300x200")
root.title("Камінь, ножиці, папір")

# Глобальні змінні для налаштувань
difficulty = StringVar(value="Легкий")
mode = StringVar(value="Класичний")
player_wins = 0
computer_wins = 0
player_moves = []

# Вибір ходу комп'ютера
computer_value = {
    "0": "Камінь",
    "1": "Ножиці",
    "2": "Папір"
}

game_window = None
settings_window = None

def info_window():
    info = Toplevel(root)
    info.title('Про нас')
    info.geometry('400x300')
    info.configure(bg='lightyellow')
    info_label = Label(info, text="Проект №2.\n Гра \"Камінь, ножиці, папір\"\nАвтори: \nТопольський Олександр\nСкрипник Анастасія\nЯнківська Богдана", font='Arial 14', bg='lightyellow')
    info_label.pack(padx=10, pady=70)

def open_settings_window():
    global settings_window
    settings_window = Toplevel(root)
    settings_window.geometry("300x300")
    settings_window.title("Налаштування гри")

    Label(settings_window, text="Виберіть рівень складності:", font="normal 12 bold").pack(pady=10)
    Radiobutton(settings_window, text="Легкий", variable=difficulty, value="Легкий").pack()
    Radiobutton(settings_window, text="Складний", variable=difficulty, value="Складний").pack()

    Label(settings_window, text="Виберіть режим гри:", font="normal 12 bold").pack(pady=10)
    Radiobutton(settings_window, text="Класичний", variable=mode, value="Класичний").pack()
    Radiobutton(settings_window, text="До 3 перемог", variable=mode, value="До 3 перемог").pack()
    Radiobutton(settings_window, text="До 10 перемог", variable=mode, value="До 10 перемог").pack()

    Button(settings_window, text="Почати гру", command=lambda: start_game(settings_window)).pack(pady=20)
    if game_window:
        game_window.destroy()

def start_game(settings_window):
    root.withdraw()
    if settings_window:
        settings_window.withdraw()
    open_game_window()
    

def open_game_window():
    game_window = Toplevel(root)
    game_window.geometry("400x500")
    game_window.title("Гра \"Камінь, ножиці, папір\"")

    global player_wins, computer_wins
    player_wins = 0
    computer_wins = 0

    game_menubar = Menu(game_window)
    game_menubar.add_command(label='Налаштування гри', command=open_settings_window)
    game_menubar.add_command(label='Вихід', command=quit)
    game_window.config(menu=game_menubar)

    # Функції для гри
    def update_score():
        score_label.config(text=f"Гравець: {player_wins} - Комп'ютер: {computer_wins}")

    def check_winner():
        if mode.get() == "До 3 перемог":
            if player_wins == 3:
                label4.config(text="Гравець виграв матч!")
                disable_buttons()
            elif computer_wins == 3:
                label4.config(text="Комп'ютер виграв матч!")
        
        if mode.get() == "До 10 перемог":
            if player_wins == 10:
                label4.config(text="Гравець виграв матч!")
                disable_buttons()
            elif computer_wins == 10:
                label4.config(text="Комп'ютер виграв матч!")
                disable_buttons()

    def disable_buttons():
        button1["state"] = "disable"
        button2["state"] = "disable"
        button3["state"] = "disable"

    def reset_game():
        global player_wins, computer_wins, timer
        button1["state"] = "active"
        button2["state"] = "active"
        button3["state"] = "active"
        label1.config(text="Гравець")
        label3.config(text="Комп'ютер")
        label4.config(text="")
        player_moves.clear()
        player_wins = 0
        computer_wins = 0
        update_score()

    def computer_choice(player_choice):
        if difficulty.get() == "Легкий":
            return computer_value[str(random.randint(0, 2))]
        else:
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

    def play(player_choice):
        global player_wins, computer_wins, timer
        c_v = computer_choice(player_choice)
        player_moves.append(player_choice)
        if mode.get() == "З таймером" and timer:
            game_window.after_cancel(timer)
        if c_v == player_choice:
            match_result = "Нічия"
        elif (player_choice == "Камінь" and c_v == "Ножиці") or \
             (player_choice == "Ножиці" and c_v == "Папір") or \
             (player_choice == "Папір" and c_v == "Камінь"):
            match_result = "Ви виграли!"
            player_wins += 1
        else:
            match_result = "Виграв комп'ютер..."
            computer_wins += 1
        label4.config(text=match_result)
        label1.config(text=player_choice)
        label3.config(text=c_v)
        update_score()
        check_winner()
        if mode.get() == "З таймером":
            timer = game_window.after(5000, play_random_move)

    def play_random_move():
        random.choice([lambda: play("Камінь"), lambda: play("Папір"), lambda: play("Ножиці")])()

    # Заголовки, кнопки, рамки
    Label(game_window, text="Rock Paper Scissor", font="normal 20 bold", fg="blue").pack(pady=20)

    frame = Frame(game_window)
    frame.pack()

    label1 = Label(frame, text="Гравець", font=10)
    label2 = Label(frame, text="VS", font="normal 10 bold")
    label3 = Label(frame, text="Комп'ютер", font=10)

    label1.pack(side=LEFT)
    label2.pack(side=LEFT)
    label3.pack()

    label4 = Label(game_window, text="Камінь, ножиці, папір!", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
    label4.pack(pady=20)

    score_label = Label(game_window, text="Гравець: 0 - Комп'ютер: 0", font="normal 12 bold")
    score_label.pack(pady=10)

    frame1 = Frame(game_window)
    frame1.pack()

    button1 = Button(frame1, text="Камінь", font=10, width=7, command=lambda: play("Камінь"))
    button2 = Button(frame1, text="Папір", font=10, width=7, command=lambda: play("Папір"))
    button3 = Button(frame1, text="Ножиці", font=10, width=7, command=lambda: play("Ножиці"))

    button1.pack(side=LEFT, padx=10)
    button2.pack(side=LEFT, padx=10)
    button3.pack(padx=10)

    Button(game_window, text="Перезапустити гру", font=10, fg="red", bg="black", command=reset_game).pack(pady=20)

# Головне вікно з кнопкою для початку гри
Label(root, text=" ").pack(pady=5)
Label(root, text="Камінь, ножиці, папір!", font="normal 15 bold", fg="blue").pack(pady=1)
Button(root, text="Почати гру", font=10, command=open_settings_window).pack(pady=5)
Button(root, text="Про нас", font=10, command=info_window).pack(pady=5)


root.mainloop()