# 📜 Changelog

---

## v0.2.0 – 2025-09-16
### ✨ New Features
- Added **version display** in Settings page.  
- Added **ℹ button** beside version to view changelog.  
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

## v0.1.0 – 2025-09-15
- Initial release with sidebar, theme system, game library, and settings page.
