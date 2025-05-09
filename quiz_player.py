import tkinter as tk
from tkinter import ttk, messagebox

def load_quizzes(filename):
    with open(filename, "r") as file:
        content = file.read().strip()

    raw_quizzes = content.split("\n\n")
    quizzes = []

    for raw in raw_quizzes:
        lines = raw.strip().split("\n")
        if len(lines) < 6:
            continue
        question = lines[0][3:]
        choices = [line[3:] for line in lines[1:5]] 
        correct = lines[5].split(":")[1].strip()
        quizzes.append((question, choices, correct))
    return quizzes

class QuizApp:
    def __init__(self, root, quizzes):
        self.root = root
        self.root.title("Cool Quiz Player")
        self.root.geometry("500x400")
        self.root.configure(bg="#e0f7fa")

        self.quizzes = quizzes
        self.q_index = 0
        self.score = 0
        self.selected = tk.StringVar()

        self.start_frame = tk.Frame(root, bg="#e0f7fa")
        self.start_frame.pack(expand=True)
        tk.Label(self.start_frame, text="Welcome to the Quiz!", font=("Helvetica", 18, "bold"), bg="#e0f7fa", fg="#006064").pack(pady=20)
        tk.Button(self.start_frame, text="Start Quiz", font=("Helvetica", 14), bg="#4dd0e1", fg="white", command=self.start_quiz).pack()

        self.quiz_frame = tk.Frame(root, bg="#e0f7fa")

        self.question_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14), bg="#e0f7fa", fg="#004d40", wraplength=450, justify="center")
        self.question_label.pack(pady=20)