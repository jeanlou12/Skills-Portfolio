import tkinter as tk
import random

def load_jokes():
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
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text="💬 " + current_joke[0])
    punchline_label.config(text="")
    show_punchline_button.config(state="normal")


def show_punchline():
    punchline_label.config(text="💬 " + current_joke[1])
    show_punchline_button.config(state="disabled")


def quit_app():
    root.destroy()


def go_to_joke_frame():
    cover_frame.pack_forget()
    joke_frame.pack(fill="both", expand=True)


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


root = tk.Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("650x400")
root.config(bg="#fdfdfd")

jokes = load_jokes()
current_joke = None


# ----------------- COVER SCREEN -----------------
cover_frame = tk.Frame(root, bg="#a76ad3")
cover_frame.pack(fill="both", expand=True)

cover_title = tk.Label(
    cover_frame, text="It's joke time!",
    font=("Arial", 28, "bold"),
    bg="#eef2ff", fg="#333"
)
cover_title.pack(pady=40)

cover_sub = tk.Label(
    cover_frame,
    text="Click below to start Alexa tell me a Joke",
    font=("Arial", 16),
    bg="#E4E4E4", fg="#555"
)
cover_sub.pack(pady=10)

start_button = rounded_button(cover_frame, "Start →", go_to_joke_frame, "#4a6bff")
start_button.pack(pady=30)


# ----------------- JOKE SCREEN -----------------
joke_frame = tk.Frame(root, bg="#fdfdfd")

title_label = tk.Label(
    joke_frame, text="Alexa, tell me a Joke!",
    font=("Arial", 20, "bold"),
    bg="#fdfdfd", fg="#333"
)
title_label.pack(pady=20)

# Speech bubble area
setup_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 15),
    wraplength=550,
    bg="#ffffff",
    fg="#000",
    bd=3,
    relief="ridge",
    padx=10,
    pady=10
)
setup_label.pack(pady=10)

punchline_label = tk.Label(
    joke_frame,
    text="",
    font=("Arial", 14, "italic"),
    wraplength=550,
    fg="#000",
    bg="#ffffff",
    bd=3,
    relief="ridge",
    padx=10,
    pady=10
)
punchline_label.pack(pady=10)

# -------- Comic Layout Buttons (Like Your Cartoon) --------
comic_frame = tk.Frame(joke_frame, bg="#fdfdfd")
comic_frame.pack(pady=25)

# Left character button
tell_button = rounded_button(comic_frame, "😄 Tell Joke", tell_joke, "#4aa9ff")
tell_button.grid(row=0, column=0, padx=20)

# Right character button
show_punchline_button = rounded_button(comic_frame, "😂 Punchline", show_punchline, "#f7b731")
show_punchline_button.grid(row=0, column=1, padx=20)
show_punchline_button.config(state="disabled")

# Bottom centered button
next_button = rounded_button(joke_frame, "➡ Next Joke", tell_joke, "#20bf6b")
next_button.pack(pady=5)

# Quit bottom
quit_button = rounded_button(joke_frame, "Quit", quit_app, "#eb3b5a")
quit_button.pack(pady=15)


root.mainloop()
