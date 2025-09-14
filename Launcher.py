import os
import json
import threading
import zipfile
from io import BytesIO
import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog
import sys
import pythoncom
# Windows shortcut creation
if sys.platform.startswith("win"):
    import winshell
    from win32com.client import Dispatch

# ------------------- Config -------------------
ROOT_DIR = "."
IMAGE_DIR = os.path.join(ROOT_DIR, "src")
os.makedirs(IMAGE_DIR, exist_ok=True)
game_progress_widgets = {}
DEFAULTNEEDS_FILE = os.path.join(ROOT_DIR, "defaultneeds.json")
DEFAULTNEEDS_VERSION_FILE = os.path.join(ROOT_DIR, "defaultneeds_version.txt")
OWNED_FILE = os.path.join(ROOT_DIR, "owned.json")
INSTALL_FOLDER_FILE = os.path.join(ROOT_DIR, "install_folder.json")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Sketchy Launcher")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())

# ------------------- Variables -------------------
provider_ip_var = ctk.StringVar(value="127.0.0.1")
install_folder_var = ctk.StringVar()

# ------------------- Logging -------------------
def log_info(msg): print(f"[INFO] {msg}")
def log_warn(msg): print(f"[WARN] {msg}")
def log_error(msg): print(f"[ERROR] {msg}")

# --- Global download queue ---
download_queue = []
queue_running = False  # Flag to avoid multiple threads

# --- Utility: Create Windows shortcut safely ---
def create_shortcut(exe_path, name):
    if not sys.platform.startswith("win") or not os.path.exists(exe_path):
        return
    def _create():
        pythoncom.CoInitialize()
        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut_path = os.path.join(desktop, f"{name}.lnk")
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            shortcut.save()
            log_info(f"Shortcut created: {shortcut_path}")
        except Exception as e:
            log_error(f"Failed to create shortcut: {e}")
        finally:
            pythoncom.CoUninitialize()
    root.after(0, _create)  # Run on main thread

# ------------------- Placeholder -------------------
def create_icon_placeholder(game_name, size=(184, 69), save_path=None):
    """
    Creates a placeholder image for a game icon.
    Typical Steam capsule size: 184x69
    """
    log_info(f"Creating icon placeholder for '{game_name}'")
    width, height = size
    img = Image.new("RGB", size, color=(60, 60, 60))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    text = game_name[:20]  # truncate if too long
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    if save_path:
        try:
            img.save(save_path)
            log_info(f"Icon placeholder saved at '{save_path}'")
        except Exception as e:
            log_error(f"Failed to save icon placeholder: {e}")
    return img

def create_header_placeholder(game_name, size=(1920, 620), save_path=None):
    """
    Creates a placeholder image for a game header/banner.
    Typical Steam hero/banner size: 600x200
    """
    log_info(f"Creating header placeholder for '{game_name}'")
    width, height = size
    img = Image.new("RGB", size, color=(80, 80, 80))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    lines, current_line = [], ""
    for word in game_name.split():
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= width - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    total_height = sum(draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] for line in lines)
    y = (height - total_height) // 2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = (width - line_width) // 2
        draw.text((x, y), line, fill=(255, 255, 255), font=font)
        y += line_height

    if save_path:
        try:
            img.save(save_path)
            log_info(f"Header placeholder saved at '{save_path}'")
        except Exception as e:
            log_error(f"Failed to save header placeholder: {e}")
    return img

def create_placeholder(game_name, size=(200, 300), save_path=None):
    log_info(f"Creating placeholder for '{game_name}'")
    width, height = size
    img = Image.new("RGB", size, color=(40, 40, 40))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    lines, current_line = [], ""
    for word in game_name.split():
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= width - 20:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] for line in lines)
    y = (height - total_height) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = (width - line_width) // 2
        draw.text((x, y), line, fill=(255,255,255), font=font)
        y += line_height

    if save_path:
        try:
            img.save(save_path)
            log_info(f"Placeholder saved at '{save_path}'")
        except Exception as e:
            log_error(f"Failed to save placeholder: {e}")
    return img

# ------------------- First launch folder -------------------
if os.path.exists(INSTALL_FOLDER_FILE):
    with open(INSTALL_FOLDER_FILE, "r", encoding="utf-8") as f:
        folder = json.load(f).get("path", "")
        install_folder_var.set(folder)
        log_info(f"Loaded install folder: {folder}")
else:
    folder = filedialog.askdirectory(title="Select Install Folder for Games")
    if folder:
        install_folder_var.set(folder)
        with open(INSTALL_FOLDER_FILE, "w", encoding="utf-8") as f:
            json.dump({"path": folder}, f, indent=4)
        log_info(f"Install folder set to: {folder}")
    else:
        log_error("No folder selected. Exiting...")
        exit()

# ------------------- Utilities -------------------
def download_or_load(app_id: int, filename: str, url: str, game_name: str, size=(200,300), type="poster") -> str:
    """
    Downloads an image if not exists; returns path.
    type: "poster", "icon", "header" — determines which placeholder to use if download fails
    """
    path = os.path.join(IMAGE_DIR, filename)
    log_info(f"Loading image for '{game_name}' (AppID: {app_id})")
    if os.path.exists(path):
        log_info(f"Found existing image: {path}")
        return path
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            log_info(f"Downloaded image for '{game_name}' to '{path}'")
            return path
        else:
            log_warn(f"Failed to download image (status {r.status_code}), using placeholder for '{game_name}'")
    except Exception as e:
        log_warn(f"Exception downloading image for '{game_name}': {e}")

    # fallback to placeholder
    if type == "poster":
        return create_placeholder(game_name, size=size, save_path=path)
    elif type == "icon":
        return create_icon_placeholder(game_name, size=size, save_path=path)
    elif type == "header":
        return create_header_placeholder(game_name, size=size, save_path=path)
    else:
        log_warn(f"Unknown type '{type}', using poster placeholder")
        return create_placeholder(game_name, size=size, save_path=path)


def load_ctk_image(path: str, size=None):
    try:
        pil_img = Image.open(path)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size) if size else ctk.CTkImage(light_image=pil_img, dark_image=pil_img)
        return ctk_img, pil_img
    except Exception as e:
        log_error(f"Failed to load CTk image from '{path}': {e}")
        return None, None


def get_game_poster(app_id, game_name, size=(200, 300)):
    filename = f"{app_id}_poster.jpg"
    url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/library_600x900.jpg"
    path = download_or_load(app_id, filename, url, game_name, size)

    ctk_img, pil_img = load_ctk_image(path, size)
    if pil_img:
        print(f"[INFO] Poster '{game_name}' original size: {pil_img.size}, display size: {size}")
    else:
        print(f"[WARN] Poster '{game_name}' failed to load")
    return ctk_img, pil_img

def get_game_header(app_id, game_name, size=(1920, 620)):
    filename = f"{app_id}_header.jpg"
    url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/library_hero.jpg"
    path = download_or_load(app_id, filename, url, game_name, size)

    ctk_img, pil_img = load_ctk_image(path, size)
    if pil_img:
        display_size = size if size else pil_img.size
        print(f"[INFO] Header '{game_name}' original size: {pil_img.size}, display size: {display_size}")
    else:
        print(f"[WARN] Header '{game_name}' failed to load")
    return ctk_img, pil_img

def get_game_icon(app_id, game_name, size=(184, 69)):
    filename = f"{app_id}_icon.jpg"
    url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_184x69.jpg"
    path = download_or_load(app_id, filename, url, game_name, size)

    ctk_img, pil_img = load_ctk_image(path, size)
    if pil_img:
        display_size = size if size else pil_img.size
        print(f"[INFO] Icon '{game_name}' original size: {pil_img.size}, display size: {display_size}")
    else:
        print(f"[WARN] Icon '{game_name}' failed to load")
    return ctk_img, pil_img
# ------------------- Data -------------------
def load_defaultneeds():
    if not os.path.exists(DEFAULTNEEDS_FILE):
        log_warn("defaultneeds.json does not exist")
        return []
    try:
        with open(DEFAULTNEEDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        log_info(f"Loaded default games list ({len(data.get('games', []))} games)")
        return data.get("games", [])
    except Exception as e:
        log_error(f"Failed to load defaultneeds.json: {e}")
        return []

def load_owned():
    if not os.path.exists(OWNED_FILE):
        log_warn("owned.json does not exist")
        return {}
    try:
        data = json.load(open(OWNED_FILE, "r", encoding="utf-8"))
        log_info(f"Loaded owned games ({len(data)})")
        return data
    except Exception as e:
        log_error(f"Failed to load owned.json: {e}")
        return {}

def save_owned(owned_dict):
    try:
        with open(OWNED_FILE, "w", encoding="utf-8") as f:
            json.dump(owned_dict, f, indent=4)
        log_info("Saved owned.json")
    except Exception as e:
        log_error(f"Failed to save owned.json: {e}")

# --- PRELOAD IMAGES IN BACKGROUND ---
def preload_images():
    default_games = load_defaultneeds()
    for g in default_games:
        app_id = g.get("app_id")
        name = g.get("name", f"Game {app_id}")
        log_info(f"Preloading images for '{name}'")
        get_game_poster(app_id, name)
        get_game_header(app_id, name)
        get_game_icon(app_id, name)

threading.Thread(target=preload_images, daemon=True).start()

# ------------------- Networking -------------------
def download_defaultneeds_file(provider_ip, provider_port="3000"):
    url_file = f"http://{provider_ip}:{provider_port}/defaultneeds.json"
    url_version = f"http://{provider_ip}:{provider_port}/defaultneeds_version"
    try:
        r = requests.get(url_file, timeout=5)
        r.raise_for_status()
        with open(DEFAULTNEEDS_FILE, "w", encoding="utf-8") as f:
            f.write(r.text)
        log_info(f"Downloaded defaultneeds.json from {url_file}")
    except Exception as e:
        if os.path.exists(DEFAULTNEEDS_FILE):
            log_warn(f"Using local defaultneeds.json (failed to download: {e})")
        else:
            log_error(f"Cannot download defaultneeds.json: {e}")
            return
    try:
        r = requests.get(url_version, timeout=5)
        r.raise_for_status()
        version = r.text.strip()
        with open(DEFAULTNEEDS_VERSION_FILE, "w", encoding="utf-8") as f:
            f.write(version)
        log_info(f"Downloaded defaultneeds version: {version}")
    except Exception as e:
        log_warn(f"Failed to download defaultneeds version: {e}")

import pythoncom

# --- Global dictionary for progress bars ---
game_progress_widgets = {}

# --- Global download queue ---
download_queue = []
queue_running = False  # Flag to avoid multiple threads

# --- Utility: Create Windows shortcut safely ---
def create_shortcut(exe_path, name):
    if not sys.platform.startswith("win") or not os.path.exists(exe_path):
        return
    def _create():
        pythoncom.CoInitialize()
        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut_path = os.path.join(desktop, f"{name}.lnk")
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = exe_path
            shortcut.WorkingDirectory = os.path.dirname(exe_path)
            shortcut.save()
            log_info(f"Shortcut created: {shortcut_path}")
        except Exception as e:
            log_error(f"Failed to create shortcut: {e}")
        finally:
            pythoncom.CoUninitialize()
    root.after(0, _create)  # Run on main thread

# --- Queue download ---
def queue_download(game):
    """Add a game to the download queue and start processing."""
    global queue_running
    if game not in download_queue:
        download_queue.append(game)
    if not queue_running:
        threading.Thread(target=process_queue, daemon=True).start()
        queue_running = True
    show_queue_page()  # Update UI

# --- Process queue ---
def process_queue():
    """Process downloads sequentially."""
    global queue_running
    while download_queue:
        game = download_queue[0]
        download_game_with_progress(game)
        download_queue.pop(0)
        show_queue_page()  # Refresh queue UI
    queue_running = False

# --- Download and extract with progress ---
def download_game_with_progress(game):
    app_id = game["app_id"]
    folder = os.path.join(install_folder_var.get(), game["name"])
    os.makedirs(folder, exist_ok=True)
    local_zip = os.path.join(folder, f"{game['name']}.zip")

    def progress_callback(val):
        if app_id in game_progress_widgets:
            widget = game_progress_widgets[app_id]
            if widget.winfo_exists():
                root.after(0, lambda: widget.set(val))

    try:
        r = requests.get(game.get("url", ""), stream=True, timeout=10)
        r.raise_for_status()
        total_length = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(local_zip, "wb") as f:
            for chunk in r.iter_content(1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_length > 0:
                        progress_callback(downloaded / total_length * 0.9)

        # Extract
        with zipfile.ZipFile(local_zip, "r") as zip_ref:
            zip_ref.extractall(folder)
        os.remove(local_zip)

        progress_callback(1.0)

        exe_path = os.path.join(folder, game.get("exe_path", game["name"] + ".exe"))
        owned = load_owned()
        owned[str(app_id)] = {"owned": True, "exe_path": exe_path, "downloaded": True}
        save_owned(owned)

        if os.path.exists(exe_path):
            create_shortcut(exe_path, game["name"])

    except Exception as e:
        log_error(f"Failed download/extract for '{game['name']}': {e}")
        progress_callback(0.0)

# ------------------- Game Actions -------------------
def claim_game(game):
    owned = load_owned()
    owned[str(game["app_id"])] = {"owned": True, "exe_path": "", "downloaded": False}
    save_owned(owned)
    log_info(f"Claimed game '{game['name']}'")
    show_shop_page()

# ------------------- Layout -------------------
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

sidebar = ctk.CTkFrame(root, width=200, fg_color="#1a1a1a", corner_radius=0)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

sidebar_label = ctk.CTkLabel(sidebar, text="Sketchy Launcher", font=("Arial", 18, "bold"))
sidebar_label.pack(pady=20)

btn_shop = ctk.CTkButton(sidebar, text="🎮 Shop", command=lambda: show_shop_page())
btn_shop.pack(pady=10, fill="x")

btn_library = ctk.CTkButton(sidebar, text="📚 Library", command=lambda: show_library_page())
btn_library.pack(pady=10, fill="x")

btn_settings = ctk.CTkButton(sidebar, text="⚙ Settings", command=lambda: show_settings_page())
btn_settings.pack(pady=10, fill="x")

btn_queue = ctk.CTkButton(sidebar, text="📥 Queue", command=lambda: show_queue_page())
btn_queue.pack(pady=10, fill="x")

content_frame = ctk.CTkFrame(root, fg_color="#222222")
content_frame.grid(row=0, column=1, sticky="nsew")

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# ------------------- Pages -------------------

# ------------------- Game Detail View -------------------
def show_game_detail(game):
    """Display the detail page for a single game with download, progress, and launch options."""
    clear_content()

    name = game["name"]
    app_id = game["app_id"]
    desc = game.get("description", "No description available.")

    # --- Load assets ---
    header_ctk, header_pil = get_game_header(app_id, name, size=(1920, 620))
    icon_ctk, icon_pil = get_game_icon(app_id, name, size=(184, 69))
    poster_ctk, poster_pil = get_game_poster(app_id, name, size=(200, 300))

    # --- Header full width ---
    if header_ctk:
        header_width = content_frame.winfo_width() or 1920
        header_height = int(header_pil.height * (header_width / header_pil.width))
        header_ctk = ctk.CTkImage(light_image=header_pil, dark_image=header_pil,
                                  size=(header_width, header_height))
        header_label = ctk.CTkLabel(content_frame, image=header_ctk, text="")
        header_label.image = header_ctk
        header_label.pack(pady=10)
        print(f"[INFO] Displaying header '{name}' size: ({header_width}, {header_height})")

    # --- Info row (icon, title, buttons) ---
    info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    info_frame.pack(fill="x", padx=20, pady=10)

    if icon_ctk:
        icon_label = ctk.CTkLabel(info_frame, image=icon_ctk, text="")
        icon_label.image = icon_ctk
        icon_label.pack(side="left", padx=10)
        print(f"[INFO] Displaying icon '{name}' size: ({icon_pil.width}, {icon_pil.height})")

    title_label = ctk.CTkLabel(info_frame, text=name, font=("Arial", 24, "bold"))
    title_label.pack(side="left", padx=10)

    # --- Progress bar ---
    progress = ctk.CTkProgressBar(content_frame, width=400)
    progress.set(0.0)
    progress.pack(pady=10)

    # Store progress bar in global dictionary
    game_progress_widgets[game["app_id"]] = progress

    # --- Action button functions ---
    owned_info = load_owned().get(str(app_id), {})

    def start_download():
        """Queue game download using global queue."""
        if game not in download_queue:
            download_queue.append(game)
        if len(download_queue) == 1:
            threading.Thread(target=process_queue, daemon=True).start()
        show_queue_page()

    if not owned_info.get("owned"):
        action_btn = ctk.CTkButton(info_frame, text="Claim",
                                   command=lambda g=game: claim_game(g))
    elif not owned_info.get("downloaded"):
        action_btn = ctk.CTkButton(info_frame, text="Download", command=start_download)
    else:
        action_btn = ctk.CTkButton(info_frame, text="Launch",
                                   command=lambda path=owned_info["exe_path"]: os.startfile(path))
    action_btn.pack(side="left", padx=10)

    # --- Settings button ---
    settings_btn = ctk.CTkButton(info_frame, text="⚙ Settings", command=show_settings_page)
    settings_btn.pack(side="right", padx=10)

    # --- Description ---
    desc_label = ctk.CTkLabel(content_frame, text=desc, font=("Arial", 16),
                              wraplength=1000, justify="left")
    desc_label.pack(padx=20, pady=20, anchor="w")

    # --- Back button ---
    back_btn = ctk.CTkButton(content_frame, text="⬅ Back", command=show_library_page)
    back_btn.pack(pady=10)

    print(f"[INFO] Showing details for '{name}' (AppID: {app_id})")

def show_shop_page():
    clear_content()

    search_entry = ctk.CTkEntry(content_frame, placeholder_text="Search Shop...")
    search_entry.pack(fill="x", padx=20, pady=10)

    canvas = ctk.CTkCanvas(content_frame, bg="#222222", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=(20,0))
    scrollbar = ctk.CTkScrollbar(content_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y", padx=(0,20))
    canvas.configure(yscrollcommand=scrollbar.set)
    grid_frame = ctk.CTkFrame(canvas, fg_color="transparent")
    window_id = canvas.create_window((0,0), window=grid_frame, anchor="nw")

    default_games = load_defaultneeds()
    owned_games = load_owned()

    def update_grid(*args):
        for widget in grid_frame.winfo_children():
            widget.destroy()
        width = canvas.winfo_width() or 800
        col_count = max(1, width // 250)
        row, col = 0, 0

        for game in default_games:
            if search_entry.get().lower() not in game["name"].lower():
                continue

            ctk_img, _ = get_game_poster(game["app_id"], game_name=game["name"])
            if not ctk_img:
                continue

            frame = ctk.CTkFrame(grid_frame, fg_color="transparent", width=220, height=340)
            frame.grid(row=row, column=col, padx=15, pady=15)
            frame.grid_propagate(False)

            btn_img = ctk.CTkButton(frame, text="", image=ctk_img, fg_color="transparent",
                                    width=200, height=300, command=lambda g=game: show_game_detail(g))
            btn_img.image = ctk_img
            btn_img.grid(row=0, column=0, padx=5, pady=5)

            col += 1
            if col >= col_count:
                col = 0
                row += 1

        grid_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window_id, width=canvas.winfo_width())

    search_entry.bind("<KeyRelease>", lambda e: update_grid())
    canvas.bind("<Configure>", update_grid)
    update_grid()


def show_library_page():
    clear_content()

    search_entry = ctk.CTkEntry(content_frame, placeholder_text="Search Library...")
    search_entry.pack(fill="x", padx=20, pady=10)

    canvas = ctk.CTkCanvas(content_frame, bg="#222222", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=(20,0))
    scrollbar = ctk.CTkScrollbar(content_frame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y", padx=(0,20))
    canvas.configure(yscrollcommand=scrollbar.set)
    grid_frame = ctk.CTkFrame(canvas, fg_color="transparent")
    window_id = canvas.create_window((0,0), window=grid_frame, anchor="nw")

    owned_games = load_owned()
    default_games = load_defaultneeds()

    def update_grid(*args):
        for widget in grid_frame.winfo_children():
            widget.destroy()
        width = canvas.winfo_width() or 800
        col_count = max(1, width // 250)
        row, col = 0, 0

        for game in default_games:
            if search_entry.get().lower() not in game["name"].lower():
                continue

            ctk_img, _ = get_game_poster(game["app_id"], game_name=game["name"])
            if not ctk_img:
                continue

            frame = ctk.CTkFrame(grid_frame, fg_color="transparent", width=220, height=340)
            frame.grid(row=row, column=col, padx=15, pady=15)
            frame.grid_propagate(False)

            btn_img = ctk.CTkButton(frame, text="", image=ctk_img, fg_color="transparent",
                                    width=200, height=300, command=lambda g=game: show_game_detail(g))
            btn_img.image = ctk_img
            btn_img.grid(row=0, column=0, padx=5, pady=5)

            col += 1
            if col >= col_count:
                col = 0
                row += 1

        grid_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window_id, width=canvas.winfo_width())

    search_entry.bind("<KeyRelease>", lambda e: update_grid())
    canvas.bind("<Configure>", update_grid)
    update_grid()


    # --- Grid Update ---
    def update_grid(*args):
        for widget in grid_frame.winfo_children():
            widget.destroy()
        width = canvas.winfo_width() or 800
        col_count = max(1, width // 250)
        row, col = 0, 0

        for game in default_games:
            owned_info = owned_games.get(str(game["app_id"]), {})
            if not owned_info.get("owned"):
                continue
            if search_entry.get().lower() not in game["name"].lower():
                continue

            ctk_img, _ = get_game_poster(game["app_id"], game_name=game["name"])
            if not ctk_img:
                continue

            frame = ctk.CTkFrame(grid_frame, fg_color="transparent", width=220, height=340)
            frame.grid(row=row, column=col, padx=15, pady=15)
            frame.grid_propagate(False)

            # Only poster button; no action button in grid
            btn_img = ctk.CTkButton(frame, text="", image=ctk_img, fg_color="transparent",
                                    width=200, height=300, command=lambda g=game: show_game_detail(g))
            btn_img.image = ctk_img
            btn_img.grid(row=0, column=0, padx=5, pady=5)

            col += 1
            if col >= col_count:
                col = 0
                row += 1

        grid_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window_id, width=canvas.winfo_width())

    search_entry.bind("<KeyRelease>", lambda e: update_grid())
    canvas.bind("<Configure>", update_grid)
    update_grid()


def show_settings_page():
    clear_content()
    label = ctk.CTkLabel(content_frame, text="⚙ Settings", font=("Arial", 20))
    label.pack(pady=20)

    ip_label = ctk.CTkLabel(content_frame, text="Provider IP:")
    ip_label.pack(pady=(10,0))
    ip_entry = ctk.CTkEntry(content_frame, textvariable=provider_ip_var)
    ip_entry.pack(pady=5)

    port_var = ctk.StringVar(value="3000")
    port_label = ctk.CTkLabel(content_frame, text="Provider Port:")
    port_label.pack(pady=(10,0))
    port_entry = ctk.CTkEntry(content_frame, textvariable=port_var)
    port_entry.pack(pady=5)

    def save_and_update():
        download_defaultneeds_file(provider_ip_var.get(), port_var.get())

    save_btn = ctk.CTkButton(content_frame, text="Save & Update", command=save_and_update)
    save_btn.pack(pady=10)

    folder_label = ctk.CTkLabel(content_frame, text="Install Folder:")
    folder_label.pack(pady=(20,0))
    folder_entry = ctk.CTkEntry(content_frame, textvariable=install_folder_var, width=400)
    folder_entry.pack(pady=5)

    def change_folder():
        folder = filedialog.askdirectory(title="Select Install Folder for Games")
        if folder:
            install_folder_var.set(folder)
            with open(INSTALL_FOLDER_FILE, "w", encoding="utf-8") as f:
                json.dump({"path": folder}, f, indent=4)

    folder_btn = ctk.CTkButton(content_frame, text="Change Folder", command=change_folder)
    folder_btn.pack(pady=5)

def show_queue_page():
    clear_content()
    label = ctk.CTkLabel(content_frame, text="📥 Download Queue", font=("Arial", 20))
    label.pack(pady=20)
    for idx, game in enumerate(download_queue):
        row_label = ctk.CTkLabel(content_frame, text=f"{idx+1}. {game['name']}")
        row_label.pack(pady=5)

download_defaultneeds_file(provider_ip_var.get())
show_shop_page()
root.mainloop()
