import json
import sys
import tkinter as tk
from tkinter import ttk
from pywebostv.connection import WebOSClient
from pywebostv.controls import (
    MediaControl,
    SystemControl,
    InputControl,
    ApplicationControl
)

TV_IP = "YOUR_LG_SMART_TV_IP"
STORE_FILE = "store.json"

# ---- Load Pairing Key ----
try:
    with open(STORE_FILE, "r") as f:
        store = json.load(f)
except:
    store = {}

# ---- Connect ----
client = WebOSClient(TV_IP, secure=True)
try:
    client.connect()
except Exception as e:
    print("Connection failed:", e)
    sys.exit()


for status in client.register(store):
    print("Status:", status)

with open(STORE_FILE, "w") as f:
    json.dump(store, f)

media = MediaControl(client)
system = SystemControl(client)
input_control = InputControl(client)
input_control.connect_input()
app_control = ApplicationControl(client)


# ---- GUI Setup ----
root = tk.Tk()
root.title("LG Mission Control 😈")
root.geometry("450x700")
root.configure(bg="#121212")
root.attributes("-topmost", True)

style = ttk.Style()
style.theme_use("clam")

# ---- Volume Slider ----
def set_volume(val):
    media.set_volume(int(float(val)))

tk.Label(root, text="Volume", bg="#121212", fg="white").pack()
volume_slider = tk.Scale(
    root, from_=0, to=100,
    orient="horizontal",
    command=set_volume,
    bg="#121212", fg="white",
    highlightthickness=0
)
volume_slider.pack(pady=5)

# ---- Navigation Pad ----
nav_frame = tk.Frame(root, bg="#121212")
nav_frame.pack(pady=10)
def key(k):
    try:
        input_control.exec_command(
            "ssap://com.webos.service.ime/sendKeyEvent",
            {"key": k}
        )
    except Exception as e:
        print("Key failed:", e)




tk.Button(nav_frame, text="↑", width=6, command=lambda: key('UP')).grid(row=0, column=1)
tk.Button(nav_frame, text="←", width=6, command=lambda: key('LEFT')).grid(row=1, column=0)
tk.Button(nav_frame, text="OK", width=6, command=lambda: key('ENTER')).grid(row=1, column=1)
tk.Button(nav_frame, text="→", width=6, command=lambda: key('RIGHT')).grid(row=1, column=2)
tk.Button(nav_frame, text="↓", width=6, command=lambda: key('DOWN')).grid(row=2, column=1)

tk.Button(root, text="Home", command=lambda: key('HOME')).pack(pady=3)
tk.Button(root, text="Back", command=lambda: key('BACK')).pack(pady=3)

# ---- Playback ----
tk.Button(root, text="Play", command=media.play).pack(pady=3)
tk.Button(root, text="Pause", command=media.pause).pack(pady=3)
tk.Button(root, text="Stop", command=media.stop).pack(pady=3)

# ---- Power ----
tk.Button(root, text="Power Off", command=system.power_off, bg="red").pack(pady=10)

# ---- HDMI Dropdown (FIXED VERSION) ----
try:
    response = client.request("ssap://tv/getExternalInputList")
    inputs = response["devices"]
    input_names = [inp['label'] for inp in inputs]
except Exception as e:
    print("Could not fetch inputs:", e)
    inputs = []
    input_names = []

def switch_input(choice):
    for inp in inputs:
        if inp['label'] == choice:
            input_control.set_input(inp['id'])

if input_names:
    tk.Label(root, text="Input Source", bg="#121212", fg="white").pack()
    selected_input = tk.StringVar(root)
    selected_input.set(input_names[0])
    tk.OptionMenu(root, selected_input, *input_names, command=switch_input).pack(pady=5)

# ---- App Launcher ----
apps = app_control.list_apps()

tk.Label(root, text="Launch App", bg="#121212", fg="white").pack()

def launch_app(app_id):
    app_control.launch(app_id)

for app in apps[:6]:
    tk.Button(
        root,
        text=app['title'],
        command=lambda a=app['id']: launch_app(a)
    ).pack(pady=2)

# ---- Keyboard Shortcuts ----
root.bind("<Up>", lambda e: key('UP'))
root.bind("<Down>", lambda e: key('DOWN'))
root.bind("<Left>", lambda e: key('LEFT'))
root.bind("<Right>", lambda e: key('RIGHT'))
root.bind("<Return>", lambda e: key('ENTER'))
root.bind("m", lambda e: media.mute(True))

root.mainloop()

