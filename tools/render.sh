#!/usr/bin/env bash
#
# Render a reveal.js deck to per-slide PNG images for video assembly.
#
# Pipeline:
#   HTML  →  (decktape)  →  PDF  →  (pdftoppm)  →  slide-NN.png
#
# Prereqs (macOS):
#   brew install poppler
#   npm install -g decktape           # or: npx decktape
#
# Usage:
#   ./tools/render.sh chapters/chapter20.html out/ch20/slides
#
# The output directory will contain: slide-01.png, slide-02.png, ...
# At 200 dpi, each PNG is 1920x1080-ish (reveal.js 1280x720 * 1.5).

set -euo pipefail

HTML="${1:?usage: render.sh <html> <out_dir> [dpi]}"
OUT_DIR="${2:?usage: render.sh <html> <out_dir> [dpi]}"
DPI="${3:-200}"

if [[ ! -f "$HTML" ]]; then
    echo "error: $HTML not found" >&2
    exit 1
fi

mkdir -p "$OUT_DIR"
PDF="$OUT_DIR/deck.pdf"

# --- Step 1: HTML → PDF via decktape ---
echo "[1/2] rendering HTML to PDF with decktape..."
if command -v decktape &>/dev/null; then
    DECKTAPE="decktape"
else
    echo "decktape not on PATH; falling back to npx (will download on first run)"
    DECKTAPE="npx -y decktape"
fi

# Decktape reads the local HTML and its relative assets directly.
# Use file:// to ensure relative ../assets paths resolve.
ABS_HTML="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"

$DECKTAPE reveal \
    --size 1920x1080 \
    "file://$ABS_HTML" \
    "$PDF"

# --- Step 2: PDF → per-slide PNG ---
echo "[2/2] converting PDF to PNG at ${DPI} dpi..."
if ! command -v pdftoppm &>/dev/null; then
    echo "error: pdftoppm not found. install poppler: brew install poppler" >&2
    exit 1
fi

pdftoppm -png -r "$DPI" "$PDF" "$OUT_DIR/slide"

# pdftoppm outputs slide-1.png, slide-2.png, ... (no zero-padding).
# Rename to slide-01.png etc. for stable sorting.
echo "normalising filenames..."
cd "$OUT_DIR"
for f in slide-*.png; do
    [[ -e "$f" ]] || continue
    n="${f#slide-}"; n="${n%.png}"
    printf -v padded "%02d" "$n"
    new="slide-${padded}.png"
    [[ "$f" != "$new" ]] && mv "$f" "$new"
done

count=$(ls slide-*.png 2>/dev/null | wc -l | tr -d ' ')
echo "done · ${count} slides → $OUT_DIR"
