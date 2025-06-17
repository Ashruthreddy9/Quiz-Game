import tkinter as tk
from tkinter import messagebox
import random

# Sample question bank
question_bank = {
    "Science": [
        {"question": "What planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
        {"question": "What is the chemical symbol for water?", "options": ["H2O", "O2", "CO2", "NaCl"], "answer": "H2O"}
    ],
    "Math": [
        {"question": "What is 12 x 12?", "options": ["144", "154", "124", "134"], "answer": "144"},
        {"question": "What is the square root of 81?", "options": ["9", "8", "7", "6"], "answer": "9"}
    ]
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("750x500")
        self.root.configure(bg="#f0f8ff")

        self.score = 0
        self.time_left = 15
        self.current_q_index = 0
        self.selected_category = None
        self.questions = []
        self.user_answers = []
        self.timer_id = None

        self.start_screen()

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def start_screen(self):
        self.cancel_timer()
        self.clear_screen()

        tk.Label(self.root, text="🎯 Welcome to the Quiz Game!", font=("Arial", 22, "bold"), bg="#f0f8ff").pack(pady=30)
        tk.Label(self.root, text="Choose a Category", font=("Arial", 16), bg="#f0f8ff").pack(pady=10)

        for category in question_bank:
            tk.Button(self.root, text=category, font=("Arial", 14), width=20,
                      command=lambda c=category: self.start_quiz(c)).pack(pady=5)

    def start_quiz(self, category):
        self.selected_category = category
        self.questions = random.sample(question_bank[category], len(question_bank[category]))
        self.current_q_index = 0
        self.score = 0
        self.user_answers = []
        self.quiz_screen()

    def quiz_screen(self):
        self.cancel_timer()
        self.clear_screen()

        question_data = self.questions[self.current_q_index]
        self.time_left = 15

        tk.Label(self.root, text=f"Category: {self.selected_category}", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)
        tk.Label(self.root, text=f"Question {self.current_q_index + 1} of {len(self.questions)}", font=("Arial", 12), bg="#f0f8ff").pack()

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}s", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="red")
        self.timer_label.pack(pady=5)

        tk.Label(self.root, text=question_data["question"], font=("Arial", 16, "bold"), wraplength=650, bg="#f0f8ff").pack(pady=20)

        self.selected_option = tk.StringVar()
        for opt in question_data["options"]:
            tk.Radiobutton(self.root, text=opt, variable=self.selected_option, value=opt,
                           font=("Arial", 14), bg="#f0f8ff").pack(anchor="w", padx=150)

        tk.Button(self.root, text="Submit", font=("Arial", 14), bg="#007acc", fg="white",
                  command=self.submit_answer).pack(pady=20)

        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.submit_answer()

    def submit_answer(self):
        self.cancel_timer()

        answer = self.selected_option.get() if self.selected_option.get() else "Not answered"
        correct = self.questions[self.current_q_index]["answer"]
        question_text = self.questions[self.current_q_index]["question"]

        self.user_answers.append((question_text, answer, correct))
        if answer == correct:
            self.score += 1

        self.current_q_index += 1
        if self.current_q_index < len(self.questions):
            self.quiz_screen()
        else:
            self.result_screen()

    def result_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="🎉 Quiz Completed!", font=("Arial", 22, "bold"), bg="#f0f8ff").pack(pady=30)
        tk.Label(self.root, text=f"Your Score: {self.score} / {len(self.questions)}", font=("Arial", 16), bg="#f0f8ff").pack(pady=10)

        tk.Button(self.root, text="Review Answers", font=("Arial", 14), command=self.review_answers).pack(pady=10)
        tk.Button(self.root, text="Play Again", font=("Arial", 14), command=self.start_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.root.quit).pack(pady=5)

    def review_answers(self):
        self.clear_screen()

        tk.Label(self.root, text="📘 Review Answers", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(frame, bg="#f0f8ff")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, (question, user_ans, correct_ans) in enumerate(self.user_answers):
            result = "✔️" if user_ans == correct_ans else "❌"
            tk.Label(scrollable_frame, text=f"{i+1}. {question}", font=("Arial", 12, "bold"), wraplength=650, bg="#f0f8ff").pack(anchor="w", padx=20, pady=5)
            tk.Label(scrollable_frame, text=f"Your Answer: {user_ans} {result}", font=("Arial", 12), bg="#f0f8ff").pack(anchor="w", padx=40)
            if user_ans != correct_ans:
                tk.Label(scrollable_frame, text=f"Correct Answer: {correct_ans}", font=("Arial", 12), bg="#f0f8ff").pack(anchor="w", padx=60)

        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14), command=self.start_screen).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
