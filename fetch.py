#!/usr/bin/env python3
"""从 tiger-code.com 重新抓取字根表数据和字体，更新 table.html 与 data.json。"""
import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PAGE_URL = "https://www.tiger-code.com/docs/comparisonTable"
FONT_URL = "https://assets.tiger-code.com/fonts/TumanPUA.ttf"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read()


def parse_rows(page: str) -> list[list[str]]:
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S)
    data = []
    for r in rows[1:]:  # 跳过表头
        cells = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells]
        if len(cells) == 4:
            data.append(cells)
    return data


def clean_pron(pron: str) -> str:
    """主根发音只保留拼音，去掉中文注释（如「bìng 病字头」→「bìng」）。"""
    s = re.sub(r"[㐀-䶿一-鿿豈-﫿]", "", pron)
    return re.sub(r"\s+", " ", s).strip(" ,，")


def main() -> None:
    font_path = ROOT / "fonts" / "TumanPUA.ttf"
    if not font_path.exists():
        font_path.write_bytes(fetch(FONT_URL))
        print("已下载字体 fonts/TumanPUA.ttf")

    data = parse_rows(fetch(PAGE_URL).decode("utf-8"))
    for row in data:
        row[2] = clean_pron(row[2])
    (ROOT / "data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    html_path = ROOT / "table.html"
    src = html_path.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False)
    src, n = re.subn(r"const DATA = \[.*?\];\n", f"const DATA = {payload};\n", src, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("table.html 中未找到 const DATA = ... 行")
    html_path.write_text(src, encoding="utf-8")
    print(f"已更新 {len(data)} 行数据 → data.json / table.html")
    print("运行 ./build.sh 重新生成 PDF")


if __name__ == "__main__":
    main()
