import customtkinter as ctk
from pynput import keyboard
import cohere, json

with open("./env_var.json") as env:
    config_env = json.load(env)
co = cohere.Client(config_env["KEY_API"])

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
        if i["name"][:len(search)] == search:
            possible_search.append(i)
    if len(possible_search) != 0 and search != "":
        label_autocomplete.configure(text=possible_search[0]["name"][len(search):])
        label_autocomplete.place(x=(157 + 8.8 * len(search)), y=2.5)
    else:
        label_autocomplete.configure(text="")
    if key.char == "\r" and len(possible_search) != 0:
        to_do_request.set(possible_search[0]["name"] + " ")
        to_do.configure(fg_color=possible_search[0]["fg_color"], border_color=possible_search[0]["border_color"], text_color=possible_search[0]["color_text_input"])
        label_autocomplete.configure(text="", fg_color=possible_search[0]["fg_color"])
        console_box.configure(fg_color=possible_search[0]["fg_color"], border_color=possible_search[0]["border_color"], scrollbar_button_color=possible_search[0]["border_color"], scrollbar_button_hover_color=possible_search[0]["border_color"])
        console_response.configure(text_color=possible_search[0]["fg_color"])
        to_do.icursor("end")
    elif key.char == '\r':
        separator = " "
        request = to_do_request.get().strip().split(" ")
        command = request.pop(0)
        request = separator.join(request)
        if command == "cohere":
            lb_cohere_request(request)
        to_do_request.set(command + " ")
def lb_cohere_request(request):
    console_response.configure(state="normal")
    try:
        response = co.chat(message=request).text
        console_response.insert("0.0", f'Question : {request}\n\n' + response + "\n\n\n---------------------------------------------------------------------------------------------------\n\n\n")
    except:
        console_response.insert("0.0", "ERROR")
    console_response.configure(state="disabled")
class App(ctk.CTk):
    def __init__(self, title, dimension):
        super().__init__()
        self.title(title)
        self.geometry(dimension)
        self.resizable(width=False, height=False)
        self.configure(fg_color="#1D1D1D")

open = False
shortcut = False
pre_key = [{"name": "cohere", "fg_color": "#FFD966", "border_color": "#CCAD33", "color_text_input": "#000000"}, {"name": "chrome", "fg_color": "#ffffff", "border_color": "#00f0f0", "color_text_input": "#000000"}, {"name": "youtube", "fg_color": "#ffffff", "border_color": "#f0f000", "color_text_input": "#000000"}]
possible_search = []

root = App("Raycast", "800x300")
to_do_request = ctk.StringVar()
to_do = ctk.CTkEntry(root, width=500, textvariable=to_do_request, placeholder_text="Hello", fg_color="#1A1A2E", border_color="#1723CA", text_color="white", font=("Monospace", 18))
to_do.pack()
to_do.bind("")
to_do.bind("<KeyRelease>", lambda key: lb_autocomplete(to_do_request.get(), key))
console_box = ctk.CTkScrollableFrame(root, border_width=2, width=720, height=200, fg_color="#1A1A2E", border_color="#1723CA", scrollbar_button_color="#1723CA", scrollbar_button_hover_color="#1723CA")
console_box.pack()
label_autocomplete = ctk.CTkLabel(root, height=20, text="", text_color="#5A5A5A", fg_color="#1A1A2E", font=("Monospace", 16))
label_autocomplete.place(x=(157 + 10 * len(to_do_request.get())), y=2)
console_response = ctk.CTkTextbox(console_box, fg_color="#2E2E2E", text_color="#1723CA", font=("Monospace", 18), activate_scrollbars=False)
console_response.pack(fill="x")

speed_key = keyboard.Listener(on_press=lb_get_key)
speed_key.start()

while not open:
    """ok"""
if open:
    root.mainloop()

#root.bind("<Control-Key-k>", lb_open_window)
#ctk.CTkFrame(app).grid(row=0, column=0)
