# Interview Prep HTML Generator

A Python tool that generates a bilingual (Japanese/Chinese) interview preparation HTML page from local structured data files (YAML or Markdown). Edit your data files, refresh the browser, and instantly preview the result — no need to regenerate with AI every time.

## Features

- **Live preview** — Built-in HTTP server regenerates HTML on every request. Edit files, refresh browser, done.
- **Dual format support** — Write your data in YAML or Markdown, whichever you prefer.
- **Bilingual** — Japanese and Chinese content coexist in one page, switchable via UI toggle.
- **Graceful fallback** — Missing language files or tabs are handled automatically (empty placeholders shown).
- **One-click export** — Export the final HTML via CLI flag or browser endpoint.

## Quick Start

```bash
# 1. Put your data files in ./data/
#    Naming: {tab_id}_{lang}.yaml or .md
#    tab_id: intern, work, project
#    lang: ja, zh

# 2. Start preview server
python app.py

# 3. Open browser
#    Preview:  http://127.0.0.1:8080
#    Export:   http://127.0.0.1:8080/export
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--data DIR` | Data directory path | `./data` |
| `--port PORT` | Server port | `8080` |
| `--config FILE` | Config file path | `config.yaml` |
| `--export FILE` | Export HTML to file and exit | — |

```bash
python app.py --data ./my_data --port 3000
python app.py --export output.html
```

## Data File Format

### YAML

```yaml
cards:
  - title: "データ分析インターン"
    period: "20XX.XX — 20XX.XX"
    company: "某テック企業（Example Corp）"
    tech_tags: [Python, SQL, Pandas]
    sections:
      - title: "運営データ分析"
        bullets:
          - "SQLによるデータ抽出・Pandasによるクリーニング..."
          - "A/Bテスト結果の定量評価..."
```

### Markdown

```markdown
# データ分析インターン
- period: 20XX.XX — 20XX.XX
- company: 某テック企業（Example Corp）
- tech: Python, SQL, Pandas

## 運営データ分析
- SQLによるデータ抽出・Pandasによるクリーニング...
- A/Bテスト結果の定量評価...

---

# Next Card Title
- period: ...
```

Cards are separated by `---`. Each `#` heading starts a card, `##` starts a section within the card.

## File Naming Convention

```
data/
├── intern_ja.yaml    # Internship experiences (Japanese)
├── intern_zh.yaml    # Internship experiences (Chinese)
├── work_ja.md        # Work experiences (Japanese)
├── work_zh.md        # Work experiences (Chinese)
├── project_ja.yaml   # Projects (Japanese)
└── project_zh.yaml   # Projects (Chinese)
```

Provide both `_ja` and `_zh` files for bilingual content. If only one language is provided, the other side will be left blank.

## Requirements

- Python 3.10+
- PyYAML (`pip install pyyaml`)

---

# 面试准备 HTML 生成器

一个 Python 工具，从本地结构化数据文件（YAML 或 Markdown）生成双语（日语/中文）面试准备 HTML 页面。编辑数据文件后刷新浏览器即可实时预览，无需每次都让 AI 重新生成。

## 功能特性

- **实时预览** — 内置 HTTP 服务器，每次请求自动重新生成 HTML。改完文件刷新浏览器即可。
- **双格式支持** — 支持 YAML 和 Markdown 两种输入格式，选择你喜欢的。
- **双语切换** — 日语和中文内容共存于一个页面，通过 UI 按钮切换。
- **优雅降级** — 缺少某种语言的文件或某个 Tab 的数据时，自动显示占位提示。
- **一键导出** — 通过命令行参数或浏览器端点导出最终 HTML 文件。

## 快速开始

```bash
# 1. 将数据文件放入 ./data/
#    命名规则: {tab_id}_{lang}.yaml 或 .md
#    tab_id: intern（实习）, work（工作）, project（项目）
#    lang: ja（日语）, zh（中文）

# 2. 启动预览服务器
python app.py

# 3. 打开浏览器
#    预览:  http://127.0.0.1:8080
#    导出:  http://127.0.0.1:8080/export
```

## 命令行选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--data DIR` | 数据目录路径 | `./data` |
| `--port PORT` | 服务器端口 | `8080` |
| `--config FILE` | 配置文件路径 | `config.yaml` |
| `--export FILE` | 导出 HTML 文件后退出 | — |

```bash
python app.py --data ./my_data --port 3000
python app.py --export output.html
```

## 数据文件格式

### YAML

```yaml
cards:
  - title: "数据分析实习生"
    period: "20XX.XX — 20XX.XX"
    company: "某科技公司（Example Corp）"
    tech_tags: [Python, SQL, Pandas]
    sections:
      - title: "运营数据分析"
        bullets:
          - "负责全流程数据分析：SQL提取→Pandas清洗..."
          - "基于A/B测试量化评估核心KPI变化..."
```

### Markdown

```markdown
# 数据分析实习生
- period: 20XX.XX — 20XX.XX
- company: 某科技公司（Example Corp）
- tech: Python, SQL, Pandas

## 运营数据分析
- 负责全流程数据分析：SQL提取→Pandas清洗...
- 基于A/B测试量化评估核心KPI变化...

---

# 下一张卡片标题
- period: ...
```

卡片之间用 `---` 分隔。`#` 标题开始一张卡片，`##` 标题开始卡片内的一个小节。

## 文件命名规则

```
data/
├── intern_ja.yaml    # 实习经历（日语）
├── intern_zh.yaml    # 实习经历（中文）
├── work_ja.md        # 工作经历（日语）
├── work_zh.md        # 工作经历（中文）
├── project_ja.yaml   # 项目经历（日语）
└── project_zh.yaml   # 项目经历（中文）
```

同时提供 `_ja` 和 `_zh` 文件即可实现双语。若只提供一种语言，另一种语言部分将留空。

## 环境要求

- Python 3.10+
- PyYAML (`pip install pyyaml`)
