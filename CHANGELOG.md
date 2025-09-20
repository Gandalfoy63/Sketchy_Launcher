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
