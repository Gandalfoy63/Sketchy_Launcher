## [0.3.7] - 2025-09-20

### Added
- First-run install folder setup: prompts user to select a folder and saves it to `install_folder.json`.
- `Change Folder` button in settings updates `install_folder.json` without triggering on page load.
- `install_folder.json` now stores absolute paths relative to the launcher directory.
- Default folder dialog now opens in the launcher folder for predictable behavior.
- `install_folder_var` properly uses `CTk.StringVar` with the main root to prevent Tkinter errors.

### Fixed
- Issue where `Change Folder` function ran immediately when loading the settings page.
- Tkinter `StringVar` initialization error (“Too early to create variable”) when loading install path.
- Inconsistent install folder detection when running from PyCharm versus direct launch.

### Changed
- Launcher now reads and writes install folder paths in a central JSON file next to `launcher.py`.
- Folder selection now defaults to the launcher directory rather than the current working directory.
