#!/usr/bin/env bash
# Download the fonts used by the concept diagram (all OFL licensed).
#
#   bash scripts/concept-diagram/fetch-fonts.sh
#
# Installs into ${MANZOKU_FONTS:-$HOME/.local/share/fonts/manzoku} and
# refreshes the font cache, so cairosvg can find the families by name.

set -euo pipefail

DEST="${MANZOKU_FONTS:-$HOME/.local/share/fonts/manzoku}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
mkdir -p "$DEST"

fetch_google() { # family query, output name
  local query="$1" out="$2" css url
  css=$(curl -fsSL -H "User-Agent: $UA" \
    "https://fonts.googleapis.com/css2?family=${query}&display=swap")
  url=$(grep -o 'https://[^)]*' <<<"$css" | head -1)
  [ -n "$url" ] || { echo "no font URL for $query" >&2; return 1; }
  echo "  $out"
  curl -fsSL -o "$DEST/$out" "$url"
}

echo "Fonts -> $DEST"
for w in 400 600 700 900; do
  fetch_google "Fraunces:opsz,wght@9..144,$w" "fraunces-$w.ttf"
done
for w in 400 700; do
  fetch_google "JetBrains+Mono:wght@$w" "jbm-$w.ttf"
done

# Zen Kaku Gothic New (kanji 満足 + arrows) - static files from google/fonts.
for w in Regular Medium Bold; do
  echo "  ZenKakuGothicNew-$w.ttf"
  curl -fsSL -o "$DEST/ZenKakuGothicNew-$w.ttf" \
    "https://github.com/google/fonts/raw/main/ofl/zenkakugothicnew/ZenKakuGothicNew-$w.ttf"
done

if command -v fc-cache >/dev/null 2>&1; then
  fc-cache -f "$DEST" >/dev/null 2>&1 || true
fi
echo "Done."
