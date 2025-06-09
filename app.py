import customtkinter as ctk
from pynput import keyboard
import cohere, json, webbrowser

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
        label_autocomplete.place(x=(130 + 8.8 * len(search)), y=2.5)
    else:
        label_autocomplete.configure(text="")
    if key.char == "\r" and len(possible_search) != 0:
        to_do_request.set(possible_search[0]["name"] + " ")
        to_do.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], border_color=colors[possible_search[0]["index_color"]]["border_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"])
        label_autocomplete.configure(text="", fg_color=colors[possible_search[0]["index_color"]]["fg_color"])
        console_box.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], border_color=colors[possible_search[0]["index_color"]]["border_color"], scrollbar_button_color=colors[possible_search[0]["index_color"]]["border_color"], scrollbar_button_hover_color=colors[possible_search[0]["index_color"]]["border_color"])
        tabs.configure(text_color=colors[possible_search[0]["index_color"]]["color_text_input"], segmented_button_fg_color=colors[possible_search[0]["index_color"]]["fg_color"], segmented_button_selected_color=colors[possible_search[0]["index_color"]]["border_color"], segmented_button_selected_hover_color=colors[possible_search[0]["index_color"]]["border_color"], segmented_button_unselected_color=colors[possible_search[0]["index_color"]]["fg_color"], segmented_button_unselected_hover_color=colors[possible_search[0]["index_color"]]["fg_color"])
        to_do.icursor("end")
    elif key.char == '\r':
        request = to_do_request.get().strip().split(" ")
        command = request.pop(0)
        for i in pre_key:
            if i["name"] == command:
                if i["type"] == "website":
                    separator = "+"
                    request = separator.join(request)
                    webbrowser.open(f"https://www.{i["adress"]}/{i["search_query"] + request}")
                elif i["type"] == "ia":
                    separator = " "
                    request = separator.join(request)
                    lb_cohere_request(request)
        for i in console_element_list:
            i.pack_forget()
            i.pack(fill="x", pady=10)
        to_do_request.set(command + " ")
def lb_cohere_request(request):
    console_response = ctk.CTkTextbox(console_box, fg_color="#2E2E2E", text_color=colors[pre_key[0]["index_color"]]["color_text_input"], font=("Monospace", 18), corner_radius=20)
    console_element_list.insert(0, console_response)
    try:
        response = co.chat(message=request).text
        console_response.insert("0.0", f'Question : {request}\n\n' + response)
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
pre_key = [{"name": "cohere", "type": "ia", "index_color": 2, "adress": "cohere.com", "search_query": None}, {"name": "chrome", "type": "website", "index_color": 9, "adress": "google.com", "search_query": "search?q="}, {"name": "youtube", "type": "website", "index_color": 0, "adress": "youtube.com", "search_query": "results?search_query="}]
colors = [{"fg_color": "#2E1A1A", "border_color": "#C91616", "color_text_input": "#ffffff"}, {"fb_color": "#2E221A", "border_color": "#C95516", "color_text_input": "#ffffff"}, {"fg_color": "#2E2B1A", "border_color": "#C9AF16", "color_text_input": "#ffffff"}, {"fg_color": "#1B2E1A", "border_color": "#1FC916", "color_text_input": "#ffffff"}, {"fg_color": "#1A2E2C", "border_color": "#16C9BB", "color_text_input": "#ffffff"}, {"fg_color": "#1C1A2E", "border_color": "#2516C9", "color_text_input": "#ffffff"}, {"fg_color": "#2A1A2E", "border_color": "#7316C9", "color_text_input": "#ffffff"}, {"fg_color": "#2E1A29", "border_color": "#C916A3", "color_text_input": "#ffffff"}, {"fg_color": "#2E1A1F", "border_color": "#C9164C", "color_text_input": "#ffffff"}, {"fg_color": "#BEBEBE", "border_color": "#ffffff", "color_text_input": "#000000"}]
possible_search = []
console_element_list = []

root = App("Raycast", "800x340")
tabs = ctk.CTkTabview(root, width=350, height=250, text_color="#ffffff", segmented_button_fg_color="#1A1A2E", segmented_button_selected_color="#1723CA", segmented_button_selected_hover_color="#2A34D4", segmented_button_unselected_color="#1A1A2E", segmented_button_unselected_hover_color="#2A34D4")
tabs.add("Console")
tabs.add("Options")
tabs.pack()

to_do_request = ctk.StringVar()

to_do = ctk.CTkEntry(tabs.tab("Console"), width=500, textvariable=to_do_request, placeholder_text="Hello", fg_color="#1A1A2E", border_color="#1723CA", text_color="white", font=("Monospace", 18))
to_do.pack()
to_do.bind("")
to_do.bind("<KeyRelease>", lambda key: lb_autocomplete(to_do_request.get(), key))
label_autocomplete = ctk.CTkLabel(tabs.tab("Console"), height=20, text="", text_color="#5A5A5A", fg_color="#1A1A2E", font=("Monospace", 16))
label_autocomplete.place(x=0, y=0)
console_box = ctk.CTkScrollableFrame(tabs.tab("Console"), border_width=2, width=720, height=200, fg_color="#1A1A2E", border_color="#1723CA", scrollbar_button_color="#1723CA", scrollbar_button_hover_color="#1723CA")
console_box.pack()

label_add_action = ctk.CTkLabel(tabs.tab("Options"), text="Add a command").pack()
entry_add_action = ctk.CTkEntry(tabs.tab("Options"), placeholder_text="Command's name").pack()
combo_add_action = ctk.CTkComboBox(tabs.tab("Options"), values=["Web site", "Software"], state="readonly").pack()
button_add_action = ctk.CTkButton(tabs.tab("Options"), text="Add").pack()

speed_key = keyboard.Listener(on_press=lb_get_key)
speed_key.start()

while not open:
    """waiting cmd+m"""
if open:
    root.mainloop()
