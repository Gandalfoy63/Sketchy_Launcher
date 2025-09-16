# 🎮 Sketchy Launcher

A custom game launcher built with **Python** and **CustomTkinter**.  
Supports **themes**, **icons**, and **dynamic UI** with a clean sidebar design.  

---

## ✨ Features
- 🖼️ **Sidebar with Icon-Only Buttons** (Shop, Library, Settings, Queue)  
- 🎨 **Theme System**  
  - Each theme has a `theme.json` defining colors  
  - Supports icons (`logo.png`, `shop.png`, `library.png`, `settings.png`, `queues.png`)  
  - Switch themes from the settings menu  
- 🌐 **Theme Pack Downloader**  
  - Downloads and extracts the latest theme pack from a given URL  
  - Automatically updates themes at startup  
- 📂 **Game Library**  
  - Scrollable grid with posters  
  - Search bar included  
- ⚙️ **Settings Page**  
  - Change provider IP & port  
  - Change install folder  
  - Save & update themes with one click  

---

## 📂 Project Structure
```plaintext
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
```

---

## 🎨 Themes
Each theme is stored in `themes/<ThemeName>/` and must include:

**theme.json**
```json
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
```

**Required Icons**
- `logo.png`  
- `shop.png`  
- `library.png`  
- `settings.png`  
- `queues.png`  

---

## 🚀 Installation
```bash
# Clone the repo
git clone https://github.com/YourUser/SketchyLauncher.git
cd SketchyLauncher

# Install dependencies
pip install customtkinter pillow requests

# Run the launcher
python Launcher.py
```

---

## ⚡ Usage
- **Library** → Browse and launch your games  
- **Shop** → *(planned)* Discover new games  
- **Queue** → Manage downloads/updates  
- **Settings** → Change provider, install folder, and theme  

---

## 📥 Updating Themes
1. Open **Settings**  
2. Enter the **Theme Pack URL**  
3. Click **Save & Update**  
4. Select your theme from the dropdown  

---

## 📌 Roadmap
- [ ] Add real shop backend integration  
- [ ] Improve game detail view  
- [ ] Add multiple theme sizes (small/large icons)  
- [ ] Cloud sync for owned games  
- [ ] Add mod/plugin support  
- [ ] Cross-platform support (Linux, macOS)  

---

## 📝 License
MIT License  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
