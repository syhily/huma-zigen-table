# huma-zigen-table

把 [虎码官网的字根表](https://www.tiger-code.com/docs/comparisonTable) 整理成适合打印的 A4 PDF：两列排版、每列独立表头、宋体字形、行不跨页截断、末页两列均分。

成品见 [`dist/虎码字根表.pdf`](dist/虎码字根表.pdf)。

## 排版特点

- A4 纵向，每页两列，共 4 页（241 个字根）
- 每列都有表头，行不会被分页线切断（JS 实测行高逐行分页）
- 字根 / 例字用宋体（Songti SC），私用区变体字形嵌入官方 `TumanPUA.ttf`
- 编码列等宽红色；主根发音只保留拼音，且每个拼音首字母加粗标红，对应编码首字母

## 重新生成 PDF

```bash
./build.sh
```

依赖本机安装的 Google Chrome（无头模式打印）。也可以直接双击 `table.html` 在 Chrome 中打开，打印 → 另存为 PDF（A4、边距无、勾选背景图形）。

## 官网数据更新后同步

```bash
./fetch.py && ./build.sh
```

`fetch.py` 会重新抓取官网字根表，清洗发音列（去掉中文注释），更新 `data.json` 和 `table.html` 内嵌数据；字体缺失时也会自动下载。

## 文件结构

```
table.html          排版模板（内嵌字根数据，JS 自动分页）
fetch.py            抓取官网最新数据
build.sh            用无头 Chrome 导出 PDF
fonts/TumanPUA.ttf  虎码私用区字形字体
data.json           字根数据（与 table.html 内嵌的一致）
dist/虎码字根表.pdf  生成的成品
```

## 版权说明

字根表数据与 `TumanPUA.ttf` 字体均来自 [tiger-code.com](https://www.tiger-code.com)，版权归原作者及虎码项目所有。本仓库仅提供打印友好的排版模板，供学习交流使用。
