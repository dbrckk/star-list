#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
if ! command -v pkg >/dev/null 2>&1 || [[ "$(uname -m)" != aarch64 ]]; then
 echo 'Installation réservée à Termux ARM64 (Android).' >&2; exit 1
fi
ROOT="$HOME/.freebuff-mobile"; APP="$ROOT/app"; BIN="$HOME/.local/bin"
URL='https://raw.githubusercontent.com/dbrckk/star-list/freebuff-android/mobile-app'
mkdir -p "$APP/www" "$BIN" "$ROOT/projects"; chmod 700 "$ROOT" "$ROOT/projects"
printf 'Installation des prérequis Android…\n'
pkg update -y
pkg install -y nodejs-lts tmux git curl || pkg install -y nodejs tmux git curl
fetch() { local src="$1" dest="$2"; curl --fail --location --show-error --silent --retry 3 --connect-timeout 15 "$URL/$src" -o "$dest.tmp"; test -s "$dest.tmp"; mv "$dest.tmp" "$dest"; }
fetch 'mobile-app/server.js' "$APP/server.js"
for file in index.html app.js style.css manifest.webmanifest icon.svg; do fetch "mobile-app/www/$file" "$APP/www/$file"; done
node --check "$APP/server.js" && node --check "$APP/www/app.js"
cat > "$BIN/freebuff-mobile" <<'LAUNCH'
#!/data/data/com.termux/files/usr/bin/bash
export PATH="$HOME/.local/bin:$PATH"
exec node "$HOME/.freebuff-mobile/app/server.js"
LAUNCH
cat > "$BIN/freebuff-mobile-start" <<'START'
#!/data/data/com.termux/files/usr/bin/bash
set -e
ROOT="$HOME/.freebuff-mobile"; mkdir -p "$ROOT"
if [[ -f "$ROOT/server.pid" ]]; then
  pid="$(cat "$ROOT/server.pid")"
  if [[ "$pid" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null && ps -p "$pid" -o args= | grep -Fq "$ROOT/app/server.js"; then
    echo 'Serveur Freebuff Mobile déjà actif.'
    sed -n '/CODE D.APPAIRAGE/p' "$ROOT/server.log" 2>/dev/null | tail -1
    exit 0
  fi
fi
nohup "$HOME/.local/bin/freebuff-mobile" > "$ROOT/server.log" 2>&1 < /dev/null &
echo "$!" > "$ROOT/server.pid"
chmod 600 "$ROOT/server.log" "$ROOT/server.pid"
sleep 2
if ! kill -0 "$(cat "$ROOT/server.pid")" 2>/dev/null; then cat "$ROOT/server.log"; exit 1; fi
cat "$ROOT/server.log"
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
if ! grep -Fq '# FREEBUFF_MOBILE_PATH' "$HOME/.bashrc" 2>/dev/null; then printf '\n# FREEBUFF_MOBILE_PATH\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.bashrc"; fi
if ! command -v freebuff >/dev/null 2>&1 && [[ ! -x "$BIN/freebuff" ]]; then
  echo 'Le moteur Freebuff officiel ne fonctionne pas nativement sous Android sans adaptation.'
  echo 'Port communautaire : https://github.com/LostSleepy/freebuff-android'
  read -r -p 'Installer ce port communautaire non officiel ? [o/N] : ' agree || agree=n
  if [[ "$agree" =~ ^[oOyY]$ ]]; then
    if pkg install -y glibc-repo glibc-runner; then
      if [[ -d "$ROOT/engine/.git" ]]; then git -C "$ROOT/engine" pull --ff-only
      else git clone --depth 1 https://github.com/LostSleepy/freebuff-android.git "$ROOT/engine"; fi
      npm install -g --prefix "$HOME/.local" "$ROOT/engine"
      export PATH="$BIN:$PATH"
      freebuff --version || echo 'Le binaire devra être vérifié depuis le diagnostic.'
    else echo 'Port natif non installé : paquets de compatibilité manquants.' >&2; fi
  fi
fi
mkdir -p "$HOME/.termux/boot"
cat > "$HOME/.termux/boot/start-freebuff-mobile" <<'BOOT'
#!/data/data/com.termux/files/usr/bin/bash
sleep 12
"$HOME/.local/bin/freebuff-mobile-start"
BOOT
chmod 700 "$HOME/.termux/boot/start-freebuff-mobile"
export PATH="$BIN:$PATH"
"$BIN/freebuff-mobile-start"
printf '\nINSTALLATION TERMINÉE. Ouvre http://127.0.0.1:8765 dans Chrome ou dans l’application Android.\n'
printf 'Pour le démarrage après redémarrage du téléphone : installer et ouvrir une fois Termux:Boot depuis F-Droid.\n'
