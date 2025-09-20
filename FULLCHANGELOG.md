# 📜 Changelog

All notable changes to this project will be documented in this file.
---
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
---
## [0.3.5] - 2025-09-20
### Added
- New **update check system** that fetches the latest version from GitHub (`version.json`) and prompts the user if a new version is available.
- **Update popup window** (modal) that always appears in front of the launcher, giving the choice to update now or later.
- Added **changelog support** via GitHub `CHANGELOG.md` format.

### Changed
- The **update process** now restarts the launcher automatically after downloading and replacing the file.
- Improved **settings.json auto-sync**: missing keys are now automatically added with default values.
- Consistent use of **grid/pack separation** in UI pages to avoid geometry manager conflicts.

### Fixed
- Fixed `NameError: show_update_page not defined` by implementing a proper popup function.
- Fixed issue where `version.json` returned incorrect values due to formatting.
- Fixed wrong version display inside **settings page** (now correctly shows the launcher version).
- Fixed broken **changelog link** to ensure proper GitHub navigation.
- Prevented update popup from appearing when `"coding": "1"` is set in `settings.json`.

## [0.3.1] - 2025-09-17

### Fixed
- Bug in version check that prevented automatic update detection.
- Fixed theme update download issues on first run.

## [v0.3.0] – 2025-09-17

### ✨ New Features
- **Automatic dependency installation**  
  On first run (or if dependencies are missing), the launcher will auto-install required Python packages:
  - `customtkinter`
  - `requests`
  - `Pillow` (PIL)
  - `tkhtmlview`
  - `markdown`  
  After installation, the launcher restarts itself automatically, so users never need to install anything manually.

### 🛠 Improvements
- Code cleanup in imports section – all dependencies are now managed in one place (`ensure_dependencies()` function).  
- More reliable startup, even on a fresh Python environment.

### 🐛 Fixes
- Fixed crash when running on systems without preinstalled dependencies.  
- Removed duplicate imports and streamlined bootstrap process.

---

## [v0.2.0] – 2025-09-16

### ✨ New Features
- Added **version display** in Settings page.  
- Added **ℹ button** beside version to view the changelog.  
- Introduced **update system placeholder** (`check_for_update`) to prepare for auto-updates.  
- Added `changelogsaw` setting to track if changelog has been shown after update.

### 🛠 Improvements
- **Theme Handler**
  - Automatically lists all installed themes.  
  - Added dropdown in Settings to switch between themes.  
  - Improved debug logs for theme loading.  
  - Better handling of missing `theme.json` or icons.  
- Sidebar buttons improved with proper icon scaling.  
- Themes now load icons at consistent **150x150 resolution**.

### 🐛 Fixes
- Fixed missing `DEFAULT_CHANGELOG_URL` crash.  
- Fixed crashes when no `theme.json` was found.

---

## [v0.1.0] – 2025-09-15
- Initial release with sidebar, theme system, game library, and settings page.
