import customtkinter as ctk
from pynput import keyboard
from PIL import Image
import cohere, json, webbrowser, string

def lb_vigenere(message, key, direction=1):
    chars = ' ' + string.punctuation + string.ascii_letters + string.digits
    key_index = 0
    encrypted_message = ''
    for letter in message:
        if ord(letter) == 10:
            encrypted_message += '\n'
            continue
        key_char = key[key_index % len(key)]
        key_index += 1
        offset = chars.index(key_char)
        index = chars.find(letter)
        new_index = (index + offset*direction) % len(chars)
        encrypted_message += chars[new_index]
    return encrypted_message
def lb_decrypt(message, key):
    return lb_vigenere(message, key, -1)
def lb_encrypt(message, key):
    return lb_vigenere(message, key, 1)
def lb_get_key(key):
    global opener, shortcut, possible_search
    try:
        if key.char == "m" and shortcut and not opener:
            opener = True
    except:
        if key == keyboard.Key.cmd and not opener:
            shortcut = True
def lb_autocomplete(search, key):
    possible_search = []
    for i in key_words:
        if i["name"][:len(search)] == search:
            possible_search.append(i)
    if len(possible_search) != 0 and search != "":
        label_autocomplete.configure(text=possible_search[0]["name"][len(search):])
        label_autocomplete.place(x=(130 + 8.8 * len(search)), y=8.5)
    elif search != "":
        label_autocomplete.configure(text="")
        label_autocomplete.place(x=1000, y=1000)
    else:
        label_autocomplete.configure(text="Enter a command")
        label_autocomplete.place(x=130, y=8.5)
    if key.char == "\r" and len(possible_search) != 0:
        to_do_request.set(possible_search[0]["name"] + " ")
        lb_reset_colors(possible_search)
        to_do.icursor("end")
    elif key.char == '\r':
        request = to_do_request.get().strip().split(" ")
        command = request.pop(0)
        for i in key_words:
            if i["name"] == command:
                if i["type"] == "Website":
                    lb_to_website(request, i)
                elif i["type"] == "AI":
                    lb_cohere_request(request)
        for i in console_element_list:
            i.pack_forget()
            i.pack(fill="x", pady=10)
        to_do_request.set(command + " ")
def lb_cohere_request(request):
    separator = " "
    request = separator.join(request)
    console_response = ctk.CTkTextbox(console_box, fg_color="#2E2E2E", text_color=colors[key_words[0]["index_color"]]["color_text_input"], font=("Monospace", 18), corner_radius=20)
    console_element_list.insert(0, console_response)
    try:
        response = co.chat(message=request).text
        console_response.insert("0.0", f'Question : {request}\n\n' + response)
    except:
        console_response.insert("0.0", "ERROR")
    console_response.configure(state="disabled")
def lb_to_website(request, e):
    try:
        image = Image.open(e["icon"])
    except:
        image = Image.open("./assets/img/iconDefault.jpg")
    image_comp = ctk.CTkImage(light_image=image, dark_image=image, size=(48, 48))
    console_response = ctk.CTkLabel(console_box, image=image_comp, compound="left", text=f"  Search \"{" ".join(request)}\" on {e["name"]} ({e["adress"]})", fg_color="#2E2E2E", text_color="#ffffff", font=("Monospace", 18), corner_radius=20)
    console_element_list.insert(0, console_response)
    separator = "+"
    request = separator.join(request)
    webbrowser.open(f"https://www.{e["adress"]}/{e["search_query"] + request}")
def lb_reset_colors(possible_search):
    to_do.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], border_color=colors[possible_search[0]["index_color"]]["border_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"])
    label_autocomplete.configure(text="", fg_color=colors[possible_search[0]["index_color"]]["fg_color"])
    console_box.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], border_color=colors[possible_search[0]["index_color"]]["border_color"], scrollbar_button_color=colors[possible_search[0]["index_color"]]["border_color"], scrollbar_button_hover_color=colors[possible_search[0]["index_color"]]["hover"])
    tabs.configure(text_color=colors[possible_search[0]["index_color"]]["color_text_input"], segmented_button_fg_color=colors[possible_search[0]["index_color"]]["fg_color"], segmented_button_selected_color=colors[possible_search[0]["index_color"]]["border_color"], segmented_button_selected_hover_color=colors[possible_search[0]["index_color"]]["border_color"], segmented_button_unselected_color=colors[possible_search[0]["index_color"]]["fg_color"], segmented_button_unselected_hover_color=colors[possible_search[0]["index_color"]]["hover"])
    label_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["hover"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"])
    name_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"])
    name_label.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"])
    icon_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"])
    icon_label.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"])
    combo_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"], button_color=colors[possible_search[0]["index_color"]]["fg_color"], dropdown_fg_color=colors[possible_search[0]["index_color"]]["fg_color"], dropdown_hover_color=colors[possible_search[0]["index_color"]]["hover"], dropdown_text_color=colors[possible_search[0]["index_color"]]["color_text_input"])
    color_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"], button_color=colors[possible_search[0]["index_color"]]["fg_color"], dropdown_fg_color=colors[possible_search[0]["index_color"]]["fg_color"], dropdown_hover_color=colors[possible_search[0]["index_color"]]["hover"], dropdown_text_color=colors[possible_search[0]["index_color"]]["color_text_input"])
    adress_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"])
    adress_label.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"])
    query_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"])
    query_label.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"])
    button_add_action.configure(fg_color=colors[possible_search[0]["index_color"]]["fg_color"], text_color=colors[possible_search[0]["index_color"]]["color_text_input"], border_color=colors[possible_search[0]["index_color"]]["border_color"], hover_color=colors[possible_search[0]["index_color"]]["hover"])
def lb_handle_type_action(value):
    button_add_action.pack_forget()
    if value == "Website":
        adress_add_action.pack(pady=5)
        query_add_action.pack(pady=5)
        adress_label.place(x=250, y=133)
        query_label.place(x=250, y=171)
    else:
        adress_add_action.pack_forget()
        query_add_action.pack_forget()
        adress_label.place(x=1000, y=1000)
        query_label.place(x=1000, y=1000)
    button_add_action.pack(side="bottom", pady=25)
def lb_show_placeholder(value, text, label, x, y):
    if value.get() == "":
        label.configure(text=text, font=("Monospace", 15))
        label.place(x=x, y=y)
    else:
        label.configure(text="", font=("Monospace", 1))
        label.place(x=1000, y=1000)
def lb_add_new_action():
    global index
    if name_new_action.get() != "" and icon_new_action.get() != "" and adress_new_action.get() != "" and query_new_action.get() != "":
        index = 0
        for i in range(len(colors)):
            if colors[i]["name"] == color_add_action.get():
                index = i
        key_words.append({"name": name_new_action.get(), "type": combo_add_action.get(), "index_color": index, "adress": adress_new_action.get(), "search_query": query_new_action.get(), "icon": icon_add_action.get()})
        with open("./command_info.json", "w", encoding="utf-8") as data:
            data.write(lb_encrypt(f'{key_words}', encrypt_key))
        name_new_action.set("")
        icon_new_action.set("")
        adress_new_action.set("")
        query_new_action.set("")
        lb_show_placeholder(name_new_action, "Command's name", name_label, 250, 58)
        lb_show_placeholder(icon_new_action, "Icon's path", icon_label, 250, 95)
        lb_show_placeholder(adress_new_action, "Adress", adress_label, 250, 133)
        lb_show_placeholder(query_new_action, "Search query", query_label, 250, 171)
        combo_add_action.set("Software")
        color_add_action.set("Red")
        lb_handle_type_action("Software")
    else:
        print('error')
class App(ctk.CTk):
    def __init__(self, title, dimension):
        super().__init__()
        self.title(title)
        self.geometry(dimension)
        self.resizable(width=False, height=False)
        self.configure(fg_color="#1D1D1D")

with open("./env_var.json", "r") as env:
    config_env = json.load(env)
encrypt_key = config_env["DECRYPT"]
try:
    with open("./command_info.json", "r") as data:
        if data.read() != "":
            key_words = json.loads("\"".join(lb_decrypt(data.read(), encrypt_key).split("'")))
        else:
            key_words = config_env["DEFAULT_KEY"]
except:
    key_words = config_env["DEFAULT_KEY"]
co = cohere.Client(config_env["KEY_API"])

opener = False
shortcut = False
colors = [{"name": "Red", "fg_color": "#2E1A1A", "border_color": "#C91616", "color_text_input": "#ffffff", "hover": "#7C1818"}, {"name": "Orange", "fb_color": "#2E221A", "border_color": "#C95516", "color_text_input": "#ffffff", "hover": "#7C3C18"}, {"name": "Yellow", "fg_color": "#2E2B1A", "border_color": "#C9AF16", "color_text_input": "#ffffff", "hover": "#7C6D18"}, {"name": "Green", "fg_color": "#1B2E1A", "border_color": "#1FC916", "color_text_input": "#ffffff", "hover": "#1D7C18"}, {"name": "Cyan", "fg_color": "#1A2E2C", "border_color": "#16C9BB", "color_text_input": "#ffffff", "hover": "#187C74"}, {"name": "Blue", "fg_color": "#1C1A2E", "border_color": "#2516C9", "color_text_input": "#ffffff", "hover": "#21187C"}, {"name": "Purple", "fg_color": "#2A1A2E", "border_color": "#7316C9", "color_text_input": "#ffffff", "hover": "#4F187C"}, {"name": "Pink", "fg_color": "#2E1A29", "border_color": "#C916A3", "color_text_input": "#ffffff", "hover": "#7C1866"}, {"name": "Dark pink", "fg_color": "#2E1A1F", "border_color": "#C9164C", "color_text_input": "#ffffff", "hover": "#7C1836"}, {"name": "White", "fg_color": "#BEBEBE", "border_color": "#ffffff", "color_text_input": "#000000", "hover": "#DFDFDF"}, {"name": "Black", "fg_color": "#3C3C3C", "border_color": "#000000", "color_text_input": "#ffffff", "hover": "#1E1E1E"}]
possible_search = []
console_element_list = []

root = App("Raycast", "800x340")
tabs = ctk.CTkTabview(root, width=700, height=300, text_color="#ffffff", segmented_button_fg_color="#000000", segmented_button_selected_color="#3C3C3C", segmented_button_selected_hover_color="#3C3C3C", segmented_button_unselected_color="#000000", segmented_button_unselected_hover_color="#1E1E1E")
tabs.add("Console")
tabs.add("Options")
tabs.pack()

to_do_request = ctk.StringVar()
name_new_action = ctk.StringVar()
icon_new_action = ctk.StringVar()
adress_new_action = ctk.StringVar()
query_new_action = ctk.StringVar()

to_do = ctk.CTkEntry(tabs.tab("Console"), width=500, textvariable=to_do_request, placeholder_text="Enter a command", fg_color="#000000", border_color="#3C3C3C", text_color="white", font=("Monospace", 18))
to_do.pack(pady=6)
to_do.bind("")
to_do.bind("<KeyRelease>", lambda key: lb_autocomplete(to_do_request.get(), key))
label_autocomplete = ctk.CTkLabel(tabs.tab("Console"), height=20, text="Enter a command", text_color="#5A5A5A", fg_color="#000000", font=("Monospace", 16))
label_autocomplete.place(x=130, y=8.5)
console_box = ctk.CTkScrollableFrame(tabs.tab("Console"), border_width=2, width=720, height=200, fg_color="#000000", border_color="#3C3C3C", scrollbar_button_color="#3C3C3C", scrollbar_button_hover_color="#3C3C3C")
console_box.pack(pady=6)

label_add_action = ctk.CTkLabel(tabs.tab("Options"), fg_color="#1E1E1E", text_color="#ffffff", corner_radius=10, text="Add a command", font=("Monospace", 18))
label_add_action.pack(pady=10)
name_add_action = ctk.CTkEntry(tabs.tab("Options"), fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=name_new_action, placeholder_text="Command's name", font=("Monospace", 18))
name_add_action.pack(pady=5)
name_label = ctk.CTkLabel(tabs.tab("Options"), fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Command's name", font=("Monospace", 15))
name_label.place(x=250, y=58)
icon_add_action = ctk.CTkEntry(tabs.tab("Options"), fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=icon_new_action, placeholder_text="Icon's path", font=("Monospace", 18))
icon_add_action.pack(pady=5)
icon_label = ctk.CTkLabel(tabs.tab("Options"), fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Icon's path", font=("Monospace", 15))
icon_label.place(x=250, y=95)
combo_add_action = ctk.CTkComboBox(tabs.tab("Options"), fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", button_color="#000000", dropdown_fg_color="#000000", dropdown_hover_color="#1E1E1E", dropdown_text_color="#ffffff", values=["Software", "Website"], state="readonly", font=("Monospace", 18), command=lambda value: lb_handle_type_action(value))
combo_add_action.set("Software")
combo_add_action.pack(side="left", pady=5, padx=50)
color_add_action = ctk.CTkComboBox(tabs.tab("Options"), fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", button_color="#000000", dropdown_fg_color="#000000", dropdown_hover_color="#1E1E1E", dropdown_text_color="#ffffff", values=["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "Pink", "Dark pink", "White", "Black"], font=("Monospace", 18), state="readonly")
color_add_action.set("Red")
color_add_action.pack(side="right", pady=5, padx=50)
adress_add_action = ctk.CTkEntry(tabs.tab("Options"), fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=adress_new_action, placeholder_text="Adress", font=("Monospace", 18))
adress_add_action.pack_forget()
adress_label = ctk.CTkLabel(tabs.tab("Options"), fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Adress", font=("Monospace", 15))
adress_label.pack_forget()
query_add_action = ctk.CTkEntry(tabs.tab("Options"), fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", width=200, textvariable=query_new_action, placeholder_text="Search query", font=("Monospace", 18))
query_add_action.pack_forget()
query_label = ctk.CTkLabel(tabs.tab("Options"), fg_color="#000000", text_color="#5A5A5A", width=10, height=10, text="Search query", font=("Monospace", 15))
query_label.pack_forget()
button_add_action = ctk.CTkButton(tabs.tab("Options"), border_width=2, fg_color="#000000", text_color="#ffffff", border_color="#3C3C3C", hover_color="#1E1E1E", text="Add", font=("Monospace", 18), cursor="hand2", command=lb_add_new_action)
button_add_action.pack(side="bottom", pady=25)
name_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(name_new_action, "Command's name", name_label, 250, 58))
icon_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(icon_new_action, "Icon's path", icon_label, 250, 95))
adress_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(adress_new_action, "Adress", adress_label, 250, 133))
query_add_action.bind("<KeyRelease>", lambda key: lb_show_placeholder(query_new_action, "Search query", query_label, 250, 171))

speed_key = keyboard.Listener(on_press=lb_get_key)
speed_key.start()

while not opener:
    """waiting cmd+m"""
if opener:
    root.mainloop()
