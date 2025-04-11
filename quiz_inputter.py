print("=== WELCOME TO QUIZ BUILDER ===")

quizzes = []

while True:
    question = input("Enter your question: ")
    choices = [input(f"Choice {i + 1}") for i in range(4)]
    correct = int(input(" Which one is correct? (1 - 4): "))

    