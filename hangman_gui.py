import tkinter as tk
from tkinter import messagebox
import random
import os

# Kiểm tra file words.txt tồn tại không
if not os.path.exists("words.txt"):
    print("⚠️ Lỗi: Không tìm thấy file 'words.txt' trong thư mục hiện tại!")
    exit()

print(">>> Game đang chạy...")

class HangmanGame:
    def __init__(self, word_file='words.txt'):
        self.word_file = word_file
        self.words = self.load_words()
        self.reset_game()

    def load_words(self):
        with open(self.word_file, 'r') as f:
            return [line.strip().upper() for line in f if line.strip()]

    def reset_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong = 6

    def guess_letter(self, letter):
        letter = letter.upper()
        if letter in self.guessed_letters or not letter.isalpha() or len(letter) != 1:
            return False
        self.guessed_letters.add(letter)
        if letter not in self.word:
            self.wrong_guesses += 1
        return True

    def get_display_word(self):
        return ' '.join([c if c in self.guessed_letters else '_' for c in self.word])

    def is_won(self):
        return all(c in self.guessed_letters for c in self.word)

    def is_lost(self):
        return self.wrong_guesses >= self.max_wrong

# ---------------- GUI ------------------

def draw_hangman():
    canvas.delete("all")
    # Cột treo
    canvas.create_line(50, 250, 150, 250)  # Đế
    canvas.create_line(100, 250, 100, 50)  # Cột đứng
    canvas.create_line(100, 50, 200, 50)   # Cột ngang
    canvas.create_line(200, 50, 200, 80)   # Dây treo

    if game.wrong_guesses > 0:
        canvas.create_oval(180, 80, 220, 120)  # Đầu
    if game.wrong_guesses > 1:
        canvas.create_line(200, 120, 200, 180)  # Thân
    if game.wrong_guesses > 2:
        canvas.create_line(200, 130, 170, 160)  # Tay trái
    if game.wrong_guesses > 3:
        canvas.create_line(200, 130, 230, 160)  # Tay phải
    if game.wrong_guesses > 4:
        canvas.create_line(200, 180, 170, 210)  # Chân trái
    if game.wrong_guesses > 5:
        canvas.create_line(200, 180, 230, 210)  # Chân phải

def update_ui():
    word_label.config(text=game.get_display_word())
    wrong_label.config(text=f"Số lần sai: {game.wrong_guesses}/{game.max_wrong}")
    draw_hangman()
    entry_letter.delete(0, tk.END)

    if game.is_won():
        messagebox.showinfo("Chiến thắng", "Bạn đã thắng!")
        disable_input()
    elif game.is_lost():
        messagebox.showinfo("Thua cuộc", f"Bạn đã thua! Từ đúng là: {game.word}")
        disable_input()

def disable_input():
    entry_letter.config(state='disabled')
    btn_guess.config(state='disabled')

def enable_input():
    entry_letter.config(state='normal')
    btn_guess.config(state='normal')

def guess():
    letter = entry_letter.get().strip()
    if game.guess_letter(letter):
        update_ui()

def reset():
    game.reset_game()
    enable_input()
    update_ui()

# ---------------- Khởi chạy ------------------

game = HangmanGame()

window = tk.Tk()
window.title("Game Hangman - Treo cổ")

word_label = tk.Label(window, text="", font=("Arial", 24))
word_label.pack(pady=10)

wrong_label = tk.Label(window, text="", font=("Arial", 14))
wrong_label.pack()

canvas = tk.Canvas(window, width=300, height=300)
canvas.pack()

frame_input = tk.Frame(window)
frame_input.pack(pady=10)

entry_letter = tk.Entry(frame_input, width=5, font=("Arial", 18))
entry_letter.pack(side="left")

btn_guess = tk.Button(frame_input, text="Đoán", command=guess)
btn_guess.pack(side="left", padx=5)

btn_reset = tk.Button(window, text="Chơi lại", command=reset)
btn_reset.pack(pady=10)

reset()
window.mainloop()
