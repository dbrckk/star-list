#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

# Freebuff Mobile: user-initiated bootstrap, then auto-start via RUN_COMMAND.
if ! command -v pkg >/dev/null 2>&1 || [[ "$(uname -m)" != aarch64 ]]; then
  printf 'Termux ARM64 requis (Android, sans root).\n' >&2
  exit 1
fi
ROOT="$HOME/.freebuff-mobile"
APP="$ROOT/app"
BIN="$HOME/.local/bin"
URL='https://raw.githubusercontent.com/dbrckk/star-list/freebuff-android/mobile-app'
mkdir -p "$ROOT/projects" "$BIN"
chmod 700 "$ROOT" "$ROOT/projects"

printf '\nConfiguration automatique de Freebuff Mobile...\n'
pkg update -y
pkg install -y nodejs-lts tmux git curl || pkg install -y nodejs tmux git curl

# Transactional deployment: never replace a working app with half-downloaded assets.
STAGE="$(mktemp -d "$ROOT/stage.XXXXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/www"
fetch(){
  local src="$1" dest="$2"
  curl --fail --location --show-error --silent --retry 3 --connect-timeout 15 \
    --max-time 90 "$URL/$src" -o "$dest"
  [[ -s "$dest" ]] || { echo "Fichier vide : $src" >&2; exit 1; }
}
fetch 'mobile-app/server.js' "$STAGE/server.js"
for file in index.html app.js style.css manifest.webmanifest icon.svg; do
  fetch "mobile-app/www/$file" "$STAGE/www/$file"
done
node --check "$STAGE/server.js"
node --check "$STAGE/www/app.js"
[[ -s "$STAGE/www/index.html" && -s "$STAGE/www/style.css" ]] || exit 1

cat > "$BIN/freebuff-mobile" <<'LAUNCH'
#!/data/data/com.termux/files/usr/bin/bash
export PATH="$HOME/.local/bin:$PATH"
exec node "$HOME/.freebuff-mobile/app/server.js"
LAUNCH
cat > "$BIN/freebuff-mobile-start" <<'START'
#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
ROOT="$HOME/.freebuff-mobile"
mkdir -p "$ROOT"
# Local health probe prevents launching duplicate daemons after crashes/restarts.
if curl --max-time 2 --silent --fail -o /dev/null http://127.0.0.1:8765/; then
  echo 'Freebuff Mobile est déjà actif.'
  exit 0
fi
if [[ -f "$ROOT/server.pid" ]]; then
  pid="$(cat "$ROOT/server.pid")"
  if [[ "$pid" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null && ps -p "$pid" -o args= | grep -Fq "$ROOT/app/server.js"; then
    echo 'Service déjà en démarrage.'
    exit 0
  fi
fi
nohup "$HOME/.local/bin/freebuff-mobile" > "$ROOT/server.log" 2>&1 < /dev/null &
echo "$!" > "$ROOT/server.pid"
chmod 600 "$ROOT/server.log" "$ROOT/server.pid"
sleep 2
if ! kill -0 "$(cat "$ROOT/server.pid")" 2>/dev/null; then
  echo 'Le serveur ne démarre pas. Regarde le journal local:' >&2
  tail -n 14 "$ROOT/server.log" >&2
  exit 1
fi
printf 'Service prêt : http://127.0.0.1:8765\n'
grep 'CODE D.APPAIRAGE' "$ROOT/server.log" 2>/dev/null | tail -1 || true
START
cat > "$BIN/freebuff-mobile-stop" <<'STOP'
#!/data/data/com.termux/files/usr/bin/bash
p="$HOME/.freebuff-mobile/server.pid"
if [[ -f "$p" ]]; then
  pid="$(cat "$p")"
  if [[ "$pid" =~ ^[0-9]+$ ]] && ps -p "$pid" -o args= | grep -Fq "$HOME/.freebuff-mobile/app/server.js"; then kill "$pid"; fi
  rm -f "$p"
fi
STOP
chmod 700 "$BIN/freebuff-mobile" "$BIN/freebuff-mobile-start" "$BIN/freebuff-mobile-stop"
if ! grep -Fq '# FREEBUFF_MOBILE_PATH' "$HOME/.bashrc" 2>/dev/null; then
  printf '\n# FREEBUFF_MOBILE_PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"
fi

# Requires a one-time explicit opt-in because it lets permitted third-party apps
# invoke commands inside Termux. Android separately checks RUN_COMMAND permission.
PROPS="$HOME/.termux/termux.properties"
mkdir -p "$(dirname "$PROPS")"
if ! grep -Eq '^[[:space:]]*allow-external-apps[[:space:]]*=[[:space:]]*true[[:space:]]*$' "$PROPS" 2>/dev/null; then
  printf '\nAutoriser Freebuff Mobile à redémarrer son service sans ouvrir Termux ?\n'
  printf 'Android demandera aussi la permission RUN_COMMAND. [o/N] : '
  read -r opt || opt=n
  if [[ "$opt" =~ ^[oOyY]$ ]]; then
    sed -i '/^[[:space:]]*allow-external-apps[[:space:]]*=/d' "$PROPS" 2>/dev/null || true
    printf '\nallow-external-apps=true\n' >> "$PROPS"
    chmod 600 "$PROPS"
    echo 'Paramètre Termux activé. Autorise ensuite RUN_COMMAND dans Android.'
  fi
fi

if ! PATH="$BIN:$PATH" command -v freebuff >/dev/null 2>&1 && [[ ! -x "$BIN/freebuff" ]]; then
  echo 'Le client officiel Linux ARM64 ne fonctionne pas seul dans Termux.'
  echo 'Port communautaire NON OFFICIEL : https://github.com/LostSleepy/freebuff-android'
  printf 'Installer ce port sur ton téléphone ? [o/N] : '
  read -r agree || agree=n
  if [[ "$agree" =~ ^[oOyY]$ ]]; then
    pkg install -y glibc-repo glibc-runner
    if [[ -d "$ROOT/engine/.git" ]]; then
      echo 'Port déjà présent : pas de mise à jour automatique de code tiers.'
    else
      git clone --depth 1 https://github.com/LostSleepy/freebuff-android.git "$ROOT/engine"
    fi
    npm install -g --prefix "$HOME/.local" "$ROOT/engine"
    PATH="$BIN:$PATH" freebuff --version || echo 'Vérifie le moteur via freebuff android-doctor.' >&2
  fi
fi

# Optional Termux:Boot extension will execute this script after a phone reboot.
mkdir -p "$HOME/.termux/boot"
cat > "$HOME/.termux/boot/start-freebuff-mobile" <<'BOOT'
#!/data/data/com.termux/files/usr/bin/bash
sleep 12
"$HOME/.local/bin/freebuff-mobile-start"
BOOT
chmod 700 "$HOME/.termux/boot/start-freebuff-mobile"

# Activate the validated app only after every staged file is ready.
BACKUP="$ROOT/app.previous"
if [[ -d "$APP" ]]; then
  rm -rf "$BACKUP"
  mv "$APP" "$BACKUP"
fi
if ! mv "$STAGE" "$APP"; then
  if [[ -d "$BACKUP" && ! -e "$APP" ]]; then mv "$BACKUP" "$APP"; fi
  exit 1
fi
trap - EXIT

export PATH="$BIN:$PATH"
"$BIN/freebuff-mobile-stop" || true
"$BIN/freebuff-mobile-start"
printf '\nInstallation terminée. Reviens dans Freebuff Mobile sur Android.\n'
printf 'Le premier appairage demande un code, ensuite le téléphone reste associé.\n'
printf 'Démarrage au boot facultatif : installe et ouvre Termux:Boot une seule fois.\n'
