#!/usr/bin/env bash
# 用本机 Chrome 无头模式把 table.html 导出为 A4 PDF
set -euo pipefail
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
  echo "未找到 Google Chrome: $CHROME" >&2
  exit 1
fi

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=20000 \
  --print-to-pdf="dist/虎码字根表.pdf" \
  "file://$PWD/table.html" 2>/dev/null

echo "已生成 dist/虎码字根表.pdf"
