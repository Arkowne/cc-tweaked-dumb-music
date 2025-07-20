Voici ton **README.md** prêt à être exporté.
Copie ce contenu et enregistre-le dans un fichier nommé `README.md` :

---

````markdown
# 🎵 ComputerCraft MIDI Player via Redstone Relay

A small project to play `.mid` songs converted into `.dumb` files through `redstone_relay` devices on a **ComputerCraft** computer.

---

## 📥 Installation

### 1️⃣ Download the main program

On your **ComputerCraft** computer, simply run:

```lua
wget https://raw.githubusercontent.com/Arkowne/cc-tweaked-dumb-music/refs/heads/main/dumb.lua dumb
````

---

## 📝 Usage

### Basic Command:

```lua
dumb <file.dumb> <delay> [wait]
```

* `<file.dumb>` : The binary file generated from a `.mid`.
* `<delay>` : The delay in seconds between each line (e.g., `0.125`).
* `wait` (optional) : Waits for a redstone signal before starting.

---

### Example:

```lua
dumb fallen_down.dumb 0.014 wait
```

This will play the file `fallen_down.dumb` at 0.014s per line and will wait for a redstone signal on the bottom side of your computer before starting.

---

## 🔧 Configuring the first relay number

You will have to configure the number of the first wired modem (your modems should be called redstone_relays_n).

```cct
set dumb.firstRelay <your_first_relay_number>
```

Example:

```cct
set dumb.firstRelay 12
```

This will make the program start from `redstone_relay_37` rather than `redstone_relay_0`.

---

## 🎼 Generate a `.dumb` from a `.mid`

Use the web converter at [https://arkowne.github.io/cc-tweaked-dumb-music](https://arkowne.github.io/cc-tweaked-dumb-music).

Or use the provided Python script in this repository to convert a MIDI file into `.dumb` (do `pip install mido` before):

```bash
python3 mid2dumb.py
```

Customize the parameters in `convert.py` (BPM, subdivisions, note min/max, etc.).

---

## 🚨 Requirements

* **ComputerCraft** installed
* **Redstone Relay** devices wired from `redstone_relay_0` to `redstone_relay_N` (36 relays required)
* **Peripheral cable** connected to the relays

---


