import tkinter as tk
from tkinter import ttk, messagebox

def load_quizzes(filename):
    with open(filename, "r") as file:
        content = file.read().strip()

    raw_quizzes = content.split("\n\n")
    quizzes = []