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
        
        self.root.geometry("800x600")  
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

        self.question_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14), bg="#e0f7fa", fg="#004d40", wraplength=750, justify="center")
        self.question_label.pack(pady=20)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.quiz_frame, text="", variable=self.selected, value=chr(65 + i),
                                font=("Helvetica", 12), bg="#e0f7fa", fg="#006064", anchor="w")
            rb.pack(anchor="center", pady=2)
            self.radio_buttons.append(rb)

        self.progress = ttk.Progressbar(self.quiz_frame, length=500, mode='determinate', maximum=100)
        self.progress.pack(pady=20)

        self.next_button = tk.Button(self.quiz_frame, text="Next", font=("Helvetica", 14), bg="#26c6da", fg="white", command=self.next_question)
        self.next_button.pack(pady=20)

    def start_quiz(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack(expand=True)
        self.load_question()

    def load_question(self):
        if self.q_index < len(self.quizzes):
            question, choices, _ = self.quizzes[self.q_index]
            self.question_label.config(text=f"Q{self.q_index + 1}: {question}")
            self.selected.set(None)
            for i, choice in enumerate(choices):
                self.radio_buttons[i].config(text=f"{chr(65 + i)}. {choice}", value=chr(65 + i))
            self.progress["value"] = (self.q_index / len(self.quizzes)) * 100
        else:
            self.show_score()

    def next_question(self):
        if not self.selected.get():
            messagebox.showwarning("No selection", "Please choose an answer before continuing.")
            return

        _, _, correct = self.quizzes[self.q_index]
        if self.selected.get() == correct:
            self.score += 1

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