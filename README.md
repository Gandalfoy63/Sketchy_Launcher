🎮 Sketchy Launcher

A custom game launcher built with Python and CustomTkinter.
Supports themes, icons, and dynamic UI with a clean sidebar design.


---

✨ Features

🖼️ Sidebar with Icon-Only Buttons (Shop, Library, Settings, Queue)

🎨 Theme System

Each theme has a theme.json defining colors.

Supports icons (logo.png, shop.png, library.png, settings.png, queues.png).

Switch themes from the settings menu.


🌐 Theme Pack Downloader

Downloads and extracts the latest theme pack from a given URL.

Automatically updates themes at startup.


📂 Game Library

Scrollable grid with posters.

Search bar included.


⚙️ Settings Page

Change provider IP & port.

Change install folder.

Save & update themes with one click.




---

📂 Project Structure

SketchyLauncher/
├── Launcher.py          # Main application
├── settings.json        # User settings (theme URL, etc.)
├── themes/              # Installed themes
│   ├── DarkDefault/
│   │   ├── theme.json
│   │   ├── logo.png
│   │   ├── shop.png
│   │   ├── library.png
│   │   ├── settings.png
│   │   └── queues.png
│   └── ...


---

🎨 Theme Format

Each theme is stored in themes/<ThemeName>/ and must include:

theme.json

{
  "name": "DarkDefault",
  "colors": {
    "background": "#1e1e1e",
    "sidebar": "#121212",
    "main_text": "#ffffff",
    "button_bg": "#2d2d2d",
    "button_hover": "#3c3c3c",
    "button_text": "#ffffff",
    "entry_bg": "#2a2a2a",
    "entry_text": "#ffffff",
    "placeholder_text": "#aaaaaa",
    "border": "#444444",
    "accent": "#ff6600"
  }
}

Required Icons

logo.png

shop.png

library.png

settings.png

queues.png



---

🚀 Installation

1. Clone the repo:

git clone https://github.com/YourUser/SketchyLauncher.git
cd SketchyLauncher


2. Install dependencies:

pip install customtkinter pillow requests


3. Run the launcher:

python Launcher.py




---

⚡ Usage

Library → Browse and launch your games.

Shop → (planned) Discover new games.

Queue → Manage downloads/updates.

Settings → Change provider, install folder, and theme.



---

📥 Updating Themes

Open Settings.

Enter the Theme Pack URL.

Click Save & Update.

Select your theme from the dropdown.



---

📌 Roadmap

[ ] Add real shop backend integration

[ ] Improve game detail view

[ ] Add multiple theme sizes (small/large icons)

[ ] Cloud sync for owned games



---

📝 License

MIT License – feel free to use, modify, and distribute.


---