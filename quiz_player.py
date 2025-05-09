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