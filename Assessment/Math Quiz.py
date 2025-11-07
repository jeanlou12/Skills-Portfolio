import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

#FUNCTIONS 

def show_start():
    """Show Frame 1 - Start Screen."""
    frame_menu.pack_forget()
    frame_quiz.pack_forget()
    frame_start.pack(pady=60)

def show_menu():
    """Show Frame 2 - Difficulty Level Selection."""
    frame_start.pack_forget()
    frame_quiz.pack_forget()
    frame_menu.pack(pady=40)

def start_quiz(selected_level):
    """Initialize quiz and switch to Frame 3."""
    global level, score, question_num
    level = selected_level
    score = 0
    question_num = 1
    frame_menu.pack_forget()
    frame_quiz.pack(pady=30)
    next_problem()

def randomInt(level):
    """Generate random numbers based on difficulty."""
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)

def decideOperation():
    """Choose addition or subtraction."""
    return random.choice(['+', '-'])

def next_problem():
    """Display a new problem."""
    global num1, num2, operation, attempts
    num1, num2 = randomInt(level)
    operation = decideOperation()
    attempts = 0
    question_label.config(text=f"Question {question_num}/10")
    problem_label.config(text=f"{num1} {operation} {num2} =")
    answer_entry.delete(0, tk.END)
    score_label.config(text=f"Score: {score}")

def checkAnswer():
    """Check user's answer."""
    global score, question_num, attempts
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a number.")
        return

    correct_answer = num1 + num2 if operation == '+' else num1 - num2
    attempts += 1

    if user_answer == correct_answer:
        if attempts == 1:
            score += 10
            messagebox.showinfo("Correct!", "Perfect! +10 points")
        else:
            score += 5
            messagebox.showinfo("Correct!", "Good! +5 points")
        next_question()
    else:
        if attempts == 1:
            messagebox.showinfo("Try Again", "Incorrect. Try once more!")
        else:
            messagebox.showinfo("Incorrect", f"Wrong again! The correct answer was {correct_answer}.")
            next_question()

def next_question():
    """Move to next question or finish quiz."""
    global question_num
    question_num += 1
    if question_num <= 10:
        next_problem()
    else:
        show_results()

def show_results():
    """Display final results."""
    grade = (
        "A+" if score >= 90 else
        "A" if score >= 80 else
        "B" if score >= 70 else
        "C" if score >= 60 else
        "D" if score >= 50 else "F"
    )
    messagebox.showinfo("Quiz Complete", f"Your Score: {score}/100\nGrade: {grade}")
    show_menu()

# THE  MAIN WINDOW 

root = tk.Tk()
root.title("Math Quiz")
root.geometry("380x350")
root.resizable(False, False)

# -BACKGROUND IMAGE -
try:
    bg_image = Image.open("Mathematics-Wallpaper.jpg")
    bg_image = bg_image.resize((380, 350))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Background image not found or error loading image:", e)
    root.configure(bg="#edf0f2ff")

# ---------- STYLING ----------
btn_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#24ae2d",
    "fg": "white",
    "activebackground": "#3498db",
    "relief": "groove",
    "width": 25
}

# FRAME 1 IS FOR THE  START SCREEN ----------
frame_start = tk.Frame(root, bg="#e9eff6")

tk.Label(frame_start, text="WELCOME TO MATH QUIZ", font=("Arial", 20, "bold"), bg="#586fbf", fg="#c3ced8").pack(pady=5)
tk.Label(frame_start, text="Test your skills across levels!", font=("Arial", 12), bg="#e9eff6").pack(pady=1)

tk.Button(frame_start, text="Start", command=show_menu, **btn_style).pack(pady=15)
tk.Button(frame_start, text="Quit", command=root.destroy, bg="#c22312", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=1)

# FRAME 2 --
frame_menu = tk.Frame(root, bg="#e9eff6")

tk.Label(frame_menu, text="MATH QUIZ", font=("Arial", 20, "bold"), bg="#e9eff6", fg="#2e4053").pack(pady=15)
tk.Label(frame_menu, text="Choose  Level:", font=("Arial", 13), bg="#e9eff6").pack(pady=5)

tk.Button(frame_menu, text="Level 1 (1-digit)", command=lambda: start_quiz("easy"), **btn_style).pack(pady=6)
tk.Button(frame_menu, text="Level 2 (2-digit)", command=lambda: start_quiz("mid-level"), **btn_style).pack(pady=6)
tk.Button(frame_menu, text="Level 3 (4-digit)", command=lambda: start_quiz("Hard"), **btn_style).pack(pady=6)
tk.Button(frame_menu, text="Back", command=show_start, bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), width=10).pack(pady=5)

#  FRAME 3--
# There are some subtraction is you need to put underscore
frame_quiz = tk.Frame(root, bg="#e9eff6")

question_label = tk.Label(frame_quiz, text="", font=("Arial", 13, "bold"), bg="#e9eff6")
question_label.pack(pady=5)

problem_label = tk.Label(frame_quiz, text="", font=("Arial", 22, "bold"), bg="#e9eff6", fg="#34495e")
problem_label.pack(pady=10)

answer_entry = tk.Entry(frame_quiz, font=("Arial", 14), justify="center", width=10)
answer_entry.pack(pady=10)

score_label = tk.Label(frame_quiz, text="Score: 0", font=("Arial", 12), bg="#e9eff6", fg="#117a65")
score_label.pack(pady=5)


tk.Button(frame_quiz, text="Submit", command=checkAnswer, **btn_style).pack(pady=8)
tk.Button(frame_quiz, text="Back to Menu", command=show_menu, bg="#95a5a6", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=8)

# ---------- START APP ----------
show_start()
root.mainloop() 