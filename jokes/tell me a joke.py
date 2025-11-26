import tkinter as tk
import random



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
        jokes = [("Oops!", "The jokes file was not found.")]
    return jokes


def tell_joke():
    """Display a random joke setup."""
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")
    show_punchline_button.config(state="normal")


def show_punchline():
    """Display the punchline."""
    punchline_label.config(text=current_joke[1])
    show_punchline_button.config(state="disabled")


def quit_app():
    root.destroy()


def go_to_joke_frame():
    """Show joke frame and hide cover frame."""
    cover_frame.pack_forget()
    joke_frame.pack(fill="both", expand=True)


# ---------- ROUNDED BUTTON MAKER ----------

def rounded_button(parent, text, command, color):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=22,
        pady=12
    )


# ---------- MAIN WINDOW ----------

root = tk.Tk()
root.title("Alexa tell me Joke ")
root.geometry("650x400")
root.config(bg="#fdfdfd")

jokes = load_jokes()
current_joke = None

# ---------- COVER FRAME (PAGE 1) ----------

cover_frame = tk.Frame(root, bg="#eef2ff")
cover_frame.pack(fill="both", expand=True)

cover_title = tk.Label(
    cover_frame,
    text="It's joke time!",
    font=("Arial", 28, "bold"),
    bg="#eef2ff",
    fg="#333"
)
cover_title.pack(pady=40)

cover_sub = tk.Label(
    cover_frame,
    text="Click below to start the Alexa tell me Joke ",
    font=("Arial", 16),
    bg="#E4E4E4",
    fg="#555"
)
cover_sub.pack(pady=10)

start_button = rounded_button(cover_frame, "Start →", go_to_joke_frame, "#a14aff")
start_button.pack(pady=30)

# 2nd frame

# 2nd frame

joke_frame = tk.Frame(root, bg="#fdfdfd")

title_label = tk.Label(
    joke_frame,
    text="Alexa, tell me a Joke!",
    font=("Arial", 20, "bold"),
    bg="#fdfdfd",
    fg="#333"
)
title_label.pack(pady=40)   # ← increased padding to move it lower

setup_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 15),
    wraplength=600,
    bg="#fdfdfd"
)
setup_label.pack(pady=10)

punchline_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 14, "italic"),
    wraplength=600,
    fg="#555",
    bg="#fdfdfd"
)
punchline_label.pack(pady=10)

button_frame = tk.Frame(joke_frame, bg="#fdfdfd")
button_frame.pack(pady=25)

tell_button = rounded_button(button_frame, "Alexa tell me a Joke", tell_joke, "#4aa9ff")
tell_button.grid(row=0, column=0, padx=10)

show_punchline_button = rounded_button(button_frame, "Show Punchline", show_punchline, "#f7b731")
show_punchline_button.grid(row=0, column=1, padx=10)
show_punchline_button.config(state="disabled")

next_button = rounded_button(button_frame, "Next Joke", tell_joke, "#20bf6b")
next_button.grid(row=0, column=2, padx=10)

quit_button = rounded_button(joke_frame, "Quit", quit_app, "#eb3b5a")
quit_button.pack(pady=10)

# ---------- RUN APP ----------

root.mainloop()
