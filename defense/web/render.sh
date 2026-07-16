#!/bin/bash
# render.sh <htmlname-without-ext>
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
BASE="E:/University/FYDP/resources/defense/web"
NAME="$1"
rm -f "$NAME.pdf"
"$CHROME" --headless=new --disable-gpu --no-first-run --no-pdf-header-footer \
  --user-data-dir="$BASE/.chrometmp" \
  --virtual-time-budget=20000 --run-all-compositor-stages-before-draw \
  --print-to-pdf="$BASE/$NAME.pdf" \
  "file:///$BASE/$NAME.html" 2>&1 | grep -iE "written|error" | grep -v gcm | head -3
