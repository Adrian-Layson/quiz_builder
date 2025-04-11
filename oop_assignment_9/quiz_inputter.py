import os

print("=== WELCOME TO QUIZ BUILDER ===\n")

quizzes = []

while True:
    question = input("Enter your question: ")
    choices = [input(f"Choice {i + 1}: " ) for i in range(4)]
    correct = int(input(" Which one is correct? (1 - 4): "))
    
    quiz = f"Q: {question}\n"
    for i, choice in enumerate(choices, 1):
        quiz += f"{i}.{choice}\n"
    quiz += f"Answer: {correct}\n\n"

    quizzes.append(quiz)

    again = input("Wil you add another question? (y/n): ").lower()
    if again != 'y':
        print("Exiting program...")
        break

with open("quiz_entries.txt", "a") as file:
    for q in quizzes:
        file.write(q)

print("Quiz saved to quiz_entries.txt")