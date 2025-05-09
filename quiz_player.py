import tkinter as tk
from tkinter import ttk, messagebox
import pygame

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
        self.root.geometry("700x500")
        self.root.configure(bg="#e0f7fa")
        self.quizzes = quizzes
        self.q_index = 0
        self.score = 0
        self.selected = tk.StringVar()
        self.answered = False

        pygame.mixer.init()
        pygame.mixer.music.load("background.mp3")
        pygame.mixer.music.play(-1)

        self.start_frame = tk.Frame(root, bg="#e0f7fa")
        self.start_frame.pack(expand=True)
        tk.Label(self.start_frame, text="Welcome to the Quiz!", font=("Helvetica", 20, "bold"), bg="#e0f7fa", fg="#006064").pack(pady=20)
        tk.Button(self.start_frame, text="Start Quiz", font=("Helvetica", 14), bg="#4dd0e1", fg="white", command=self.start_quiz).pack()

        self.quiz_frame = tk.Frame(root, bg="#e0f7fa")

        self.question_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 16), bg="#e0f7fa", fg="#004d40", wraplength=600, justify="center")
        self.question_label.pack(pady=20)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.quiz_frame, text="", variable=self.selected, value=chr(65 + i),
                                font=("Helvetica", 14), bg="#e0f7fa", fg="#006064", anchor="w", command=self.enable_next)
            rb.pack(anchor="center", pady=5)
            self.radio_buttons.append(rb)

        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 12, "italic"), bg="#e0f7fa", fg="black")
        self.feedback_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.quiz_frame, length=400, mode='determinate')
        self.progress.pack(pady=15)

        self.next_button = tk.Button(self.quiz_frame, text="Next", font=("Helvetica", 14), bg="#26c6da", fg="white", command=self.check_answer)
        self.next_button.pack(pady=10)
        self.next_button.config(state="disabled")

    def start_quiz(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack(expand=True)
        self.load_question()

    def load_question(self):
        if self.q_index < len(self.quizzes):
            question, choices, _ = self.quizzes[self.q_index]
            self.question_label.config(text=f"Q{self.q_index + 1}: {question}")
            self.selected.set(None)
            self.feedback_label.config(text="")
            self.answered = False
            self.next_button.config(text="Check", state="disabled")
            for i, choice in enumerate(choices):
                self.radio_buttons[i].config(text=f"{chr(65 + i)}. {choice}", value=chr(65 + i), state="normal")
            self.progress["value"] = (self.q_index / len(self.quizzes)) * 100
        else:
            self.show_score()

    def enable_next(self):
        self.next_button.config(state="normal")

    def check_answer(self):
        if not self.answered:
            _, _, correct = self.quizzes[self.q_index]
            chosen = self.selected.get()
            if chosen == correct:
                self.feedback_label.config(text="Correct!", fg="green")
                self.score += 1
            else:
                self.feedback_label.config(text=f"Wrong! Correct answer: {correct}", fg="red")
            for rb in self.radio_buttons:
                rb.config(state="disabled")
            self.answered = True
            self.next_button.config(text="Next")
        else:
            self.q_index += 1
            self.load_question()

    def show_score(self):
        self.progress["value"] = 100
        messagebox.showinfo("Quiz Complete", f"You got {self.score} out of {len(self.quizzes)} correct!")
        self.root.quit()

filename = "quiz_entries.txt"
quizzes = load_quizzes(filename)
if quizzes:
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", thickness=10, troughcolor="#b2ebf2", background="#00acc1", bordercolor="#00acc1")
    app = QuizApp(root, quizzes)
    root.mainloop()
else:
    print("No quizzes found in the file.")