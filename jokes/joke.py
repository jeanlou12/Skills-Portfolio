import tkinter as tk
import random

# ---------- FUNCTIONS ----------

def load_jokes():
    """Load jokes (setup + punchline) from a text file."""
    jokes = []
    try:
        with open("randomJokes.txt", "r", encoding="utf-8") as file_handler:
            for line in file_handler:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup.strip() + "?", punchline.strip()))
    except FileNotFoundError:
        jokes = [("Oops!", "The jokes file was not found. Make sure 'randomJokes.txt' is in the same folder.")]
    return jokes


def tell_joke():
    """Display a random joke setup."""
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")
    show_punchline_button.config(state="normal")


def show_punchline():
    """Display the punchline of the current joke."""
    punchline_label.config(text=current_joke[1])
    show_punchline_button.config(state="disabled")


def quit_app():
    """Exit the application."""
    root.destroy()


# ---------- MAIN WINDOW ----------

root = tk.Tk()
root.title("Alexa - Tell Me a Joke")
root.geometry("650x400")
root.config(bg="#fdfdfd")

# Load jokes from file
jokes = load_jokes()
current_joke = None

# ---------- WIDGETS ----------

title_label = tk.Label(root, text="Alexa, tell me a Joke!", font=("Arial", 20, "bold"), bg="#fdfdfd", fg="#333")
title_label.pack(pady=20)

setup_label = tk.Label(root, text="", font=("Arial", 15), wraplength=600, bg="#fdfdfd")
setup_label.pack(pady=10)

punchline_label = tk.Label(root, text="", font=("Arial", 14, "italic"), wraplength=600, fg="#555", bg="#fdfdfd")
punchline_label.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#fdfdfd")
button_frame.pack(pady=25)

tell_button = tk.Button(button_frame, text="Alexa tell me a Joke", command=tell_joke, width=20, height=2, bg="#87CEEB")
tell_button.grid(row=0, column=0, padx=10)

show_punchline_button = tk.Button(button_frame, text="Show Punchline", command=show_punchline, width=15, height=2, bg="#FFD700", state="disabled")
show_punchline_button.grid(row=0, column=1, padx=10)

next_button = tk.Button(button_frame, text="Next Joke", command=tell_joke, width=12, height=2, bg="#90EE90")
next_button.grid(row=0, column=2, padx=10)

quit_button = tk.Button(root, text="Quit", command=quit_app, width=10, height=2, bg="#FF6347")
quit_button.pack(pady=10)

# ---------- RUN THE APP ----------
root.mainloop() 
 