import customtkinter as ctk
from pynput import keyboard

def lb_get_key(key):
    global open, shortcut
    try:
        if key.char == "m" and shortcut and not open:
            open = True
    except:
        if key == keyboard.Key.cmd and not open:
            shortcut = True

class App(ctk.CTk):
    def __init__(self, title, dimension):
        super().__init__()
        self.title(title)
        self.geometry(dimension)
        self.resizable(width=False, height=False)
        self.configure(fg_color="#1D1D1D")

open = False
shortcut = False
pre_key = ["chatgpt", "chrome", "youtube"]
possible_search = []

root = App("Raycast", "800x300")
to_do_request = ctk.StringVar()
to_do = ctk.CTkEntry(root, width=500, textvariable=to_do_request, placeholder_text="Hello", fg_color="#1A1A2E", border_color="#1723CA", text_color="white", font=("Monospace", 18))
to_do.pack()
console = ctk.CTkScrollableFrame(root, border_width=2, width=720, height=200, fg_color="#1A1A2E", border_color="#1723CA", scrollbar_button_color="#1723CA", scrollbar_button_hover_color="#2A34D4")
console.pack()
label = ctk.CTkLabel(console, text="SSSSSsss", anchor="w")
label.pack(fill="x")

speed_key = keyboard.Listener(on_press=lb_get_key)
speed_key.start()

while not open:
    """ok"""
if open:
    root.mainloop()

#root.bind("<Control-Key-k>", lb_open_window)
#ctk.CTkFrame(app).grid(row=0, column=0)