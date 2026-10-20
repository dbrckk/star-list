#!/usr/bin/env bash
# Freebuff Android: one-file installer and menu for Termux + Ubuntu PRoot.
# SPDX-License-Identifier: MIT
set -Eeuo pipefail

APP_NAME='Freebuff Android'
APP_VERSION='1.1.0'
APP_HOME="${HOME}/.freebuff-android"
APP_BIN="${HOME}/.local/bin/freebuff-android"
UBUNTU='ubuntu'

say() { printf '\n[%s] %s\n' "$APP_NAME" "$*"; }
warn() { printf '\n[ATTENTION] %s\n' "$*" >&2; }
die() { printf '\n[ERREUR] %s\n' "$*" >&2; exit 1; }
paused() { read -r -p 'Entrée pour revenir au menu… ' _ || true; }

check_termux() {
  command -v pkg >/dev/null 2>&1 || die "Cette application doit être lancée dans Termux (F-Droid), pas dans un terminal Linux classique."
  case "$(uname -m)" in
    aarch64|arm64) ;;
    *) die "Architecture non prise en charge : $(uname -m). Ce paquet cible Android ARM64." ;;
  esac
}

ubuntu_exists() {
  command -v proot-distro >/dev/null 2>&1 && proot-distro list --quiet 2>/dev/null | grep -Fxq -- "$UBUNTU"
}

inside_ubuntu() {
  proot-distro login "$UBUNTU" -- /bin/bash -lc "$1"
}

install_ubuntu_dependencies() {
  say 'Configuration Linux Ubuntu et installation du Freebuff CLI officiel.'
  # The heredoc runs as root INSIDE the isolated Ubuntu filesystem.
  proot-distro login "$UBUNTU" -- /bin/bash -se <<'INNER_INSTALL'
set -Eeuo pipefail
export DEBIAN_FRONTEND=noninteractive
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export LANG=C.UTF-8
apt-get update -qq
apt-get install -y --no-install-recommends ca-certificates curl git xz-utils tar coreutils tmux procps
# Keep public git clone functional even when the optional GitHub CLI isn't packaged.
if ! command -v gh >/dev/null 2>&1; then
  if ! apt-get install -y --no-install-recommends gh; then
    echo 'GitHub CLI absent, public git clone remains available.' >&2
  fi
fi
update-ca-certificates >/dev/null

# Official Node.js ARM64 glibc distribution, verified with SHA-256.
# Use latest v22.x patch so security patches are not pinned indefinitely.
node_dir=/opt/freebuff-node22
if [[ ! -x "$node_dir/bin/node" ]] || [[ "$("$node_dir/bin/node" --version 2>/dev/null || :)" != v22.* ]]; then
  node_tmp="$(mktemp -d)"
  trap 'rm -rf "$node_tmp"' EXIT
  curl -fsSL --retry 3 --connect-timeout 15 https://nodejs.org/dist/latest-v22.x/SHASUMS256.txt -o "$node_tmp/SHASUMS256.txt"
  archive="$(awk '$2 ~ /^node-v[0-9]+\.[0-9]+\.[0-9]+-linux-arm64\.tar\.xz$/ {print $2; exit}' "$node_tmp/SHASUMS256.txt")"
  [[ -n "$archive" ]] || { echo 'Archive Node.js ARM64 introuvable' >&2; exit 1; }
  curl -fsSL --retry 3 --connect-timeout 15 "https://nodejs.org/dist/latest-v22.x/$archive" -o "$node_tmp/$archive"
  ( cd "$node_tmp" && grep -F "  $archive" SHASUMS256.txt | sha256sum --check --status )
  mkdir -p "$node_dir"
  tar -xJf "$node_tmp/$archive" -C "$node_dir" --strip-components=1
  rm -rf "$node_tmp"
  trap - EXIT
fi
ln -sfn "$node_dir/bin/node" /usr/local/bin/node
ln -sfn "$node_dir/bin/npm" /usr/local/bin/npm
ln -sfn "$node_dir/bin/npx" /usr/local/bin/npx
npm install -g --prefix /usr/local freebuff
mkdir -p /root/projects/atelier
printf '\nNode : %s\nnpm : %s\nFreebuff :\n' "$(node --version)" "$(npm --version)"
# This check also downloads/executes the native Freebuff Linux-ARM64 binary.
freebuff --version
INNER_INSTALL
}

install_app_shortcuts() {
  mkdir -p "${HOME}/.local/bin" "${HOME}/.shortcuts" "$APP_HOME"
  local source_file target
  source_file="${BASH_SOURCE[0]}"
  target="$APP_BIN"
  if [[ "$(cd "$(dirname "$source_file")" && pwd -P)/$(basename "$source_file")" != "$(dirname "$target")/$(basename "$target")" ]]; then
    cp -- "$source_file" "$target"
  fi
  chmod 700 "$target"
  # Optional: the Termux:Widget app lists this shortcut automatically.
  printf '#!%s/bin/bash\nexec "%s"\n' "$PREFIX" "$target" > "${HOME}/.shortcuts/Freebuff Android"
  chmod 700 "${HOME}/.shortcuts/Freebuff Android"
  say 'Raccourcis créés : freebuff-android et Termux:Widget (si installé).'
}

setup() {
  check_termux
  mkdir -p "$APP_HOME"
  say 'Préparation de Freebuff sur ton téléphone Android (aucun PC nécessaire).'
  pkg update -y
  pkg install -y proot-distro git curl
  if ! ubuntu_exists; then
    say 'Installation du système Linux Ubuntu ARM64.'
    proot-distro install ubuntu:24.04 --name "$UBUNTU"
  else
    say 'Ubuntu déjà installé : réutilisation sans suppression des projets.'
  fi
  install_ubuntu_dependencies
  install_app_shortcuts
  printf 'version=%s\n' "$APP_VERSION" > "$APP_HOME/installed"
  say 'Installation terminée : sélectionne Connexion Freebuff, puis Projet.'
}

require_setup() {
  ubuntu_exists || die 'Freebuff Android n’est pas installé. Lance : bash Freebuff-Android.sh'
}

list_projects() {
  inside_ubuntu 'mkdir -p /root/projects && find /root/projects -mindepth 1 -maxdepth 1 -type d -printf "%f\n" | LC_ALL=C sort'
}

open_project() {
  local -a projects=()
  mapfile -t projects < <(list_projects)
  ((${#projects[@]})) || { warn 'Aucun projet disponible. Utilise Cloner un dépôt GitHub.'; return; }
  printf '\nProjets disponibles :\n'
  local i n selected
  for ((i=0;i<${#projects[@]};i++)); do printf ' %2d. %s\n' "$((i+1))" "${projects[i]}"; done
  read -r -p 'Numéro du projet (0 = annuler) : ' n || return
  [[ "$n" =~ ^[0-9]+$ ]] || { warn 'Numéro invalide.'; return; }
  ((10#$n > 0)) || return
  ((10#$n <= ${#projects[@]})) || { warn 'Projet inconnu.'; return; }
  selected="${projects[10#$n-1]}"
  # Directory names come from the filesystem. Avoid injecting a name into shell syntax.
  [[ "$selected" =~ ^[A-Za-z0-9._-]+$ ]] || { warn 'Nom de dossier incompatible.'; return; }
  say "Lancement de Freebuff dans $selected. (Pour quitter : Ctrl+C.)"
  proot-distro login "$UBUNTU" -- /bin/bash -lc 'export TERM=xterm-256color LANG=C.UTF-8; cd "/root/projects/$1" && exec freebuff' _ "$selected" || warn 'Freebuff s’est arrêté. Utilise Diagnostic pour vérifier l’installation.'
}

clone_project() {
  local repo folder
  read -r -p 'Dépôt GitHub (owner/repository), par ex. dbrckk/star-list : ' repo || return
  # Do not accept URLs, shell expansions, credentials, path traversal, or ref fragments.
  [[ "$repo" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || { warn 'Format attendu : propriétaire/depot (pas une URL).'; return; }
  folder="${repo#*/}"
  [[ "$folder" != '.' && "$folder" != '..' && "${repo%%/*}" != '.' && "${repo%%/*}" != '..' ]] || { warn 'Nom interdit.'; return; }
  say "Clonage de $repo dans /root/projects/$folder"
  if ! proot-distro login "$UBUNTU" -- /bin/bash -lc '
    set -e
    repo="$1"; folder="$2"
    mkdir -p /root/projects
    if [[ -e "/root/projects/$folder" ]]; then
      printf "Ce dossier existe déjà, aucun écrasement.\n" >&2
      exit 2
    fi
    if gh auth status >/dev/null 2>&1; then
      gh repo clone "$repo" "/root/projects/$folder"
    else
      git clone "https://github.com/$repo.git" "/root/projects/$folder"
    fi
  ' _ "$repo" "$folder"; then
    warn 'Clonage impossible. Pour un dépôt privé, sélectionne Connexion GitHub.'
  else
    say "Dépôt $repo disponible. Sélectionne Ouvrir un projet."
  fi
}

login_freebuff() {
  say 'La commande affiche un lien de connexion. Ouvre-le dans Chrome, puis reviens ici.'
  inside_ubuntu 'freebuff login' || warn 'Connexion non terminée. Recommence quand tu le souhaites.'
}

login_github() {
  say 'Un code de connexion apparaîtra. Ouvre https://github.com/login/device depuis ton téléphone.'
  if ! inside_ubuntu 'command -v gh' >/dev/null 2>&1; then
    warn 'GitHub CLI absent. Choisis la réparation pour tenter sa réinstallation.'
    return
  fi
  inside_ubuntu 'gh auth login --hostname github.com --git-protocol https --web' || warn 'Connexion GitHub non terminée.'
  inside_ubuntu 'gh auth setup-git' || true
}

update_freebuff() {
  say 'Mise à jour du client officiel Freebuff sans toucher aux projets.'
  inside_ubuntu 'npm install -g --prefix /usr/local freebuff && freebuff --version' || warn 'Mise à jour échouée. Connexion réseau ou registre npm à vérifier.'
}

diagnostics() {
  say 'État des composants :'
  printf 'Android : %s\n' "$(uname -m)"
  printf 'Ubuntu : '
  if ubuntu_exists; then echo 'OK'; else echo 'ABSENT'; return; fi
  inside_ubuntu 'printf "Architecture Linux : "; uname -m; printf "Node : "; node --version; printf "npm : "; npm --version; printf "Git : "; git --version; printf "Freebuff : "; freebuff --version; printf "GitHub : "; if gh auth status >/dev/null 2>&1; then echo "connecté"; else echo "non connecté"; fi' || warn 'Certains composants ne sont pas prêts.'
}

git_status_all() {
  say 'Etat Git des projets (aucune modification, aucun push).'
  proot-distro login "$UBUNTU" -- /bin/bash -lc '
    shopt -s nullglob
    for dir in /root/projects/*; do
      [[ -d "$dir/.git" || -f "$dir/.git" ]] || continue
      printf "\\n--- %s ---\\n" "${dir##*/}"
      git -C "$dir" status --short --branch || true
    done
  ' || warn 'Verification Git incomplete.'
}

menu() {
  check_termux
  require_setup
  while :; do
    printf '\n===== FREEBUFF ANDROID =====\n'
    printf ' 1. Ouvrir Freebuff dans un projet\n'
    printf ' 2. Cloner un dépôt GitHub\n'
    printf ' 3. Connexion à Freebuff\n'
    printf ' 4. Connexion GitHub (dépôts privés)\n'
    printf ' 5. Mise à jour Freebuff\n'
    printf ' 6. Diagnostic\n'\n    printf ' 7. Réparer (sans perte des projets)\n'\n    printf ' 8. Statut Git des projets\n'
    printf ' 0. Quitter\n\n'
    local choice
    read -r -p 'Ton choix : ' choice || break
    case "$choice" in
      1) open_project; paused ;;
      2) clone_project; paused ;;
      3) login_freebuff; paused ;;
      4) login_github; paused ;;
      5) update_freebuff; paused ;;
      6) diagnostics; paused ;;\n      7) setup; paused ;;\n      8) git_status_all; paused ;;
      0) break ;;
      *) warn 'Choix non reconnu.' ;;
    esac
  done
}

main() {
  case "${1:-}" in
    --help|-h) printf 'Freebuff Android %s\nUtilisation : bash Freebuff-Android.sh [--install|--repair|--menu|--diagnostic]\n' "$APP_VERSION" ;;
    --install) setup; menu ;;\n    --repair) setup ;;
    --menu) menu ;;
    --diagnostic) check_termux; require_setup; diagnostics ;;
    *)
      if ubuntu_exists && [[ -f "$APP_HOME/installed" ]]; then menu
      else setup; menu
      fi ;;
  esac
}
main "$@"