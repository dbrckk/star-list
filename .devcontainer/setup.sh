#!/usr/bin/env bash
set -Eeuo pipefail
# Runs once as remoteUser inside GitHub Codespaces; does not touch repository code.
mkdir -p "$HOME/.local" "$HOME/projects"
npm install -g --prefix "$HOME/.local" freebuff
if ! grep -Fq 'FREEBUFF_ANDROID_PATH' "$HOME/.bashrc"; then
  printf '\n# FREEBUFF_ANDROID_PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
fi
install -m 0755 .devcontainer/freebuff-mobile "$HOME/.local/bin/freebuff-mobile"
"$HOME/.local/bin/freebuff" --version
printf '\nFreebuff prêt. Dans le terminal, exécuter : freebuff-mobile\n'
