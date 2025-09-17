# 📜 Changelog

All notable changes to this project will be documented in this file.

---
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
