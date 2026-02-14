
# 📺 LG Mission Control

A desktop GUI remote controller for LG WebOS TVs built using Python and Tkinter.
Control volume, navigation, apps, playback, and input sources directly from your computer.

---

## ✨ Features

* 🎚 Volume slider control
* ⬆⬇⬅➡ Navigation pad with keyboard shortcuts
* ▶ Play / Pause / Stop media
* 🔌 HDMI input switching
* 📱 App launcher
* 🔴 Power off control
* 🌙 Clean dark-mode interface
* 🧠 Persistent pairing key storage

---

## 🛠 Tech Stack

* Python 3
* Tkinter (GUI)
* `pywebostv` (WebOS API wrapper)
* WebSocket communication

---

## 🚀 How It Works

The application connects to your LG WebOS TV over your local network using the WebOS WebSocket API.
It authenticates using a pairing key stored locally and sends control commands via the WebOS service endpoints.

---

## 📦 Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/lg-mission-control.git
cd lg-mission-control
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Set your TV IP address using an environment variable:

**Windows:**

```
set LG_TV_IP=192.168.1.50
```

**Mac/Linux:**

```
export LG_TV_IP=192.168.1.50
```

---

## ▶ Run

```
python tvremote.py
```

On first run, your TV will prompt for pairing approval.

---

## 🧠 Use Cases

* Desktop-based remote control
* Network automation experiments
* Learning WebSocket device communication
* Personal IoT control projects

---

## ⚠ Requirements

* LG WebOS TV
* TV and PC must be on same network
* "LG Connect Apps" enabled on TV

---

## 📌 Future Improvements

* Connection status indicator
* Now Playing information
* Multi-TV support
* Packaging as standalone executable
* Improved UI styling

---

