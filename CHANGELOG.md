# 📜 Changelog

All notable changes to this project will be documented in this file.

---

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
