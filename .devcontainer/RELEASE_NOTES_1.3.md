# Freebuff Android 1.3.0

- New first-install disk-space preflight (requires at least 1.5 GiB free).
- Read-only `--doctor` command: architecture, Node/npm/Freebuff versions, bounded `--help` check and project count. No token extraction/upload.
- Additional CI pseudo-terminal launch checks on Linux x64 and native ARM64.
- Repair mode preserves project directories and logins.
- Offline tests cover an existing Ubuntu, new Ubuntu, project path validation and low disk space.

**Status:** tested via simulated Termux/PRoot environments. GitHub Actions Linux integration and real Android 15/PRoot execution are separate checks, not yet confirmed by this report. Freebuff CLI is not the desktop GUI and still uses online models.
