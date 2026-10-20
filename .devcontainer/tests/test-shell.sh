#!/usr/bin/env bash
set -Eeuo pipefail
d="$(cd "$(dirname "$0")/.." && pwd)"
bash -n "$d/Freebuff-Android.sh" "$d/setup.sh" "$d/freebuff-mobile"
python3 -m json.tool "$d/devcontainer.json" >/dev/null
"$d/Freebuff-Android.sh" --help | grep -q '1.1.0'
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp/home" TEST_LOG="$tmp/log" PREFIX="$tmp/termux" PD_TEST="$tmp/present"
mkdir -p "$HOME" "$tmp/bin" "$PREFIX"
cat > "$tmp/bin/uname" <<'EOF'
#!/usr/bin/env bash
[[ "${1:-}" == -m ]] && { echo aarch64; exit; }
/usr/bin/uname "$@"
EOF
cat > "$tmp/bin/pkg" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$tmp/bin/proot-distro" <<'EOF'
#!/usr/bin/env bash
if [[ "${1:-}" == list ]]; then
  [[ "${2:-}" == --quiet ]] || exit 2
  [[ -f "$PD_TEST" ]] && echo ubuntu
  exit 0
fi
if [[ "${1:-}" == install ]]; then
  [[ "${2:-}" == ubuntu:24.04 && "${3:-}" == --name && "${4:-}" == ubuntu ]] || exit 2
  touch "$PD_TEST"
  exit 0
fi
if [[ "${1:-}" == login ]]; then
  [[ " $* " == *' /bin/bash -se '* ]] && cat >/dev/null
  exit 0
fi
exit 2
EOF
for name in uname pkg proot-distro; do chmod +x "$tmp/bin/$name"; done
printf '0\n' | PATH="$tmp/bin:$PATH" bash "$d/Freebuff-Android.sh" --install > "$tmp/out"
[[ -f "$PD_TEST" && -x "$HOME/.local/bin/freebuff-android" ]]
grep -q 'Installation terminée' "$tmp/out"
PATH="$tmp/bin:$PATH" bash "$d/Freebuff-Android.sh" --repair > "$tmp/repair"
# Menu must reject traversal (without touching network).
printf '2\nowner/../../invalid\n0\n' | bash "$d/freebuff-mobile" > "$tmp/menu"
grep -q 'Format invalide' "$tmp/menu"
printf 'Offline tests OK\n'
