import customtkinter as ctk
from pynput import keyboard

def lb_get_key(key):
    global open, shortcut, possible_search
    try:
        if key.char == "m" and shortcut and not open:
            open = True
    except:
        if key == keyboard.Key.cmd and not open:
            shortcut = True
def lb_autocomplete(search, key):
    possible_search = []
    for i in pre_key:
        if i[:len(search)] == search:
            possible_search.append(i)
    if len(possible_search) != 0 and search != "":
        label_autocomplete.configure(text=possible_search[0][len(search):])
        label_autocomplete.place(x=(157 + 8.8 * len(search)), y=2.5)
    else:
        label_autocomplete.configure(text="")
    print(possible_search)
    if key.char == "\r" and len(possible_search) != 0:
        to_do_request.set(possible_search[0] + " ")
        label_autocomplete.configure(text="")
        to_do.icursor("end")
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
to_do.bind("")
to_do.bind("<KeyRelease>", lambda key: lb_autocomplete(to_do_request.get(), key))
console = ctk.CTkScrollableFrame(root, border_width=2, width=720, height=200, fg_color="#1A1A2E", border_color="#1723CA", scrollbar_button_color="#1723CA", scrollbar_button_hover_color="#2A34D4")
console.pack()
label_autocomplete = ctk.CTkLabel(root, height=20, text="", text_color="#5A5A5A", fg_color="#1A1A2E", font=("Monospace", 16))
label_autocomplete.place(x=(157 + 10 * len(to_do_request.get())), y=2)
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
