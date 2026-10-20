#!/usr/bin/env bash
set -Eeuo pipefail
# Runs once as remoteUser inside GitHub Codespaces; does not touch repository code.
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$HOME/.local/bin" "$HOME/projects"
command -v npm >/dev/null || { echo 'Node/npm absent dans ce Codespace' >&2; exit 1; }
npm install -g --prefix "$HOME/.local" freebuff
if ! grep -Fq 'FREEBUFF_ANDROID_PATH' "$HOME/.bashrc"; then
  printf '\n# FREEBUFF_ANDROID_PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
fi
install -m 0755 "$repo_root/.devcontainer/freebuff-mobile" "$HOME/.local/bin/freebuff-mobile"
"$HOME/.local/bin/freebuff" --version
printf '\nFreebuff prêt. Dans le terminal, exécuter : freebuff-mobile\n'
