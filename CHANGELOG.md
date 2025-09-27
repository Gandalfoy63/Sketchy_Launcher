## [0.5.0] - 2025-09-27

### Added
- Provider Info page now includes **username** (`provider_user`) and **password** (`provider_pwd`) fields.
- Provider password is **hashed with SHA-256** before being appended to download URLs.
- `defaultneeds.json` and `defaultneeds_version` URLs now include credentials: `cred='<user>'&pwd='<hashed_pwd>'`.
- **Info logs** added for provider credentials (username and hashed password) for debugging.
- Saved credentials persist in `settings.json` and are editable via the UI.

### Fixed
- Credential variables (`user` and `pwd_hashed`) are now **globally available** for networking and download functions.
- Download functions now properly **authenticate with the provider server** using credentials.
- Local `defaultneeds.json` is used as a **fallback** if the download fails.
