"""Generate the bilingual HTML page from parsed data."""

from parser import TabData, Card, Section

TEMPLATE_CSS = """\
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', sans-serif; background: #f5f5f3; color: #1a1a18; padding: 2rem 1rem; }
.wrapper { max-width: 860px; margin: 0 auto; }
h1 { font-size: 20px; font-weight: 500; margin-bottom: 1.5rem; color: #1a1a18; }
.top-tabs { display: flex; gap: 8px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.top-tab { padding: 7px 18px; border: 0.5px solid #888780; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; background: #fff; color: #5f5e5a; transition: all 0.15s; }
.top-tab:hover { background: #f1efe8; }
.top-tab.active { background: #EEEDFE; color: #3C3489; border-color: transparent; }
.page { display: none; }
.page.visible { display: block; }
.exp-card { border: 0.5px solid #d3d1c7; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; background: #fff; }
.exp-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px; flex-wrap: wrap; gap: 8px; }
.exp-title { font-size: 16px; font-weight: 500; color: #1a1a18; }
.exp-period { font-size: 12px; color: #888780; padding-top: 3px; }
.exp-company { font-size: 13px; color: #5f5e5a; margin-bottom: 10px; }
.tech-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.tech-tag { background: #f1efe8; border: 0.5px solid #d3d1c7; border-radius: 8px; font-size: 11px; padding: 2px 8px; color: #5f5e5a; font-family: 'SF Mono', 'Consolas', monospace; }
.section-label { font-size: 14px; font-weight: 600; letter-spacing: 0.04em; color: #3a3a38; margin: 16px 0 8px; padding-bottom: 6px; border-bottom: 1px solid #d3d1c7; }
.section-label:first-of-type { margin-top: 0; }
.bullet-list { list-style: none; padding: 0; margin: 0; }
.bullet-item { display: flex; gap: 8px; padding: 5px 0; font-size: 14px; color: #1a1a18; line-height: 1.65; border-bottom: 0.5px solid #e8e6df; }
.bullet-item:last-child { border-bottom: none; }
.bullet-dot { color: #888780; padding-top: 1px; min-width: 12px; }
.lang-toggle { display: flex; gap: 4px; margin-bottom: 1rem; }
.lang-btn { padding: 4px 12px; font-size: 12px; border: 0.5px solid #888780; border-radius: 8px; cursor: pointer; background: #fff; color: #5f5e5a; transition: all 0.15s; }
.lang-btn.active { background: #B5D4F4; color: #0C447C; border-color: transparent; }
.ja { display: block; }
.zh { display: none; }
.lang-zh .ja { display: none; }
.lang-zh .zh { display: block; }
.empty-placeholder { padding: 2rem; text-align: center; color: #888780; font-size: 13px; }
"""

TEMPLATE_JS = """\
function showPage(id, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('visible'));
  document.querySelectorAll('.top-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('visible');
  btn.classList.add('active');
}
function setLang(lang) {
  const root = document.querySelector('.wrapper');
  if (lang === 'zh') {
    root.classList.add('lang-zh');
    document.getElementById('btn-zh').classList.add('active');
    document.getElementById('btn-ja').classList.remove('active');
  } else {
    root.classList.remove('lang-zh');
    document.getElementById('btn-ja').classList.add('active');
    document.getElementById('btn-zh').classList.remove('active');
  }
}
"""


def _esc(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _render_card(card_ja: Card | None, card_zh: Card | None) -> str:
    """Render a single exp-card with bilingual content."""
    # Use whichever card is available for shared fields
    ref = card_ja or card_zh
    if not ref:
        return ""

    title_ja = _esc(card_ja.title) if card_ja else ""
    title_zh = _esc(card_zh.title) if card_zh else ""
    period = _esc(ref.period)
    company_ja = _esc(card_ja.company) if card_ja else ""
    company_zh = _esc(card_zh.company) if card_zh else ""
    tech_tags = ref.tech_tags

    parts = []
    parts.append('<div class="exp-card">')
    parts.append('  <div class="exp-header">')
    parts.append('    <div class="exp-title">')
    parts.append(f'      <span class="ja">{title_ja}</span>')
    parts.append(f'      <span class="zh">{title_zh}</span>')
    parts.append("    </div>")
    parts.append(f'    <div class="exp-period">{period}</div>')
    parts.append("  </div>")
    parts.append('  <div class="exp-company">')
    parts.append(f'    <span class="ja">{company_ja}</span>')
    parts.append(f'    <span class="zh">{company_zh}</span>')
    parts.append("  </div>")

    if tech_tags:
        parts.append('  <div class="tech-row">')
        for tag in tech_tags:
            parts.append(f'    <span class="tech-tag">{_esc(tag)}</span>')
        parts.append("  </div>")

    # Sections — zip ja and zh sections together
    ja_sections = card_ja.sections if card_ja else []
    zh_sections = card_zh.sections if card_zh else []
    max_sections = max(len(ja_sections), len(zh_sections))

    for i in range(max_sections):
        sec_ja = ja_sections[i] if i < len(ja_sections) else None
        sec_zh = zh_sections[i] if i < len(zh_sections) else None

        sec_title_ja = _esc(sec_ja.title) if sec_ja else ""
        sec_title_zh = _esc(sec_zh.title) if sec_zh else ""

        margin = ' style="margin-top:18px;"' if i > 0 else ""
        parts.append(f'  <div class="section-label"{margin}>')
        parts.append(f'    <span class="ja">{chr(0x2460 + i)} {sec_title_ja}</span>')
        parts.append(f'    <span class="zh">{chr(0x2460 + i)} {sec_title_zh}</span>')
        parts.append("  </div>")

        ja_bullets = sec_ja.bullets if sec_ja else []
        zh_bullets = sec_zh.bullets if sec_zh else []
        max_bullets = max(len(ja_bullets), len(zh_bullets))

        if max_bullets > 0:
            parts.append('  <ul class="bullet-list">')
            for j in range(max_bullets):
                b_ja = _esc(ja_bullets[j]) if j < len(ja_bullets) else ""
                b_zh = _esc(zh_bullets[j]) if j < len(zh_bullets) else ""
                parts.append('    <li class="bullet-item">')
                parts.append('      <span class="bullet-dot">&middot;</span>')
                parts.append(f'      <span class="ja">{b_ja}</span>')
                parts.append(f'      <span class="zh">{b_zh}</span>')
                parts.append("    </li>")
            parts.append("  </ul>")

    parts.append("</div>")
    return "\n".join(parts)


def generate_html(
    title: str,
    tabs: list[dict],
    data: dict[str, dict[str, TabData | None]],
) -> str:
    """
    Generate the full HTML page.

    Args:
        title: Page title
        tabs: List of tab configs, each with id, icon, label_ja, label_zh
        data: {tab_id: {"ja": TabData|None, "zh": TabData|None}}
    """
    # Tab buttons
    tab_buttons = []
    for i, tab in enumerate(tabs):
        active = " active" if i == 0 else ""
        label_ja = _esc(tab["label_ja"])
        label_zh = _esc(tab["label_zh"])
        tab_buttons.append(
            f'    <button class="top-tab{active}" onclick="showPage(\'{tab["id"]}\', this)">'
            f'{tab["icon"]} '
            f'<span class="ja">{label_ja}</span>'
            f'<span class="zh">{label_zh}</span>'
            f"</button>"
        )

    # Tab pages
    tab_pages = []
    for i, tab in enumerate(tabs):
        visible = " visible" if i == 0 else ""
        tab_data = data.get(tab["id"], {})
        ja_tab = tab_data.get("ja")
        zh_tab = tab_data.get("zh")

        page_parts = [f'  <div id="page-{tab["id"]}" class="page{visible}">']

        if not ja_tab and not zh_tab:
            page_parts.append(
                '    <div class="empty-placeholder">'
                '<span class="ja">データなし / ファイル未提供</span>'
                '<span class="zh">暂无数据 / 文件未提供</span>'
                "</div>"
            )
        else:
            ja_cards = ja_tab.cards if ja_tab else []
            zh_cards = zh_tab.cards if zh_tab else []
            max_cards = max(len(ja_cards), len(zh_cards))

            for j in range(max_cards):
                c_ja = ja_cards[j] if j < len(ja_cards) else None
                c_zh = zh_cards[j] if j < len(zh_cards) else None
                page_parts.append(_render_card(c_ja, c_zh))

        page_parts.append("  </div>")
        tab_pages.append("\n".join(page_parts))

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(title)}</title>
<style>
{TEMPLATE_CSS}
</style>
</head>
<body>
<div class="wrapper">
  <h1>{_esc(title)}</h1>

  <div class="top-tabs">
{chr(10).join(tab_buttons)}
  </div>

  <div class="lang-toggle">
    <button class="lang-btn active" id="btn-ja" onclick="setLang('ja')">日本語</button>
    <button class="lang-btn" id="btn-zh" onclick="setLang('zh')">中文</button>
  </div>

{chr(10).join(tab_pages)}

</div>
<script>
{TEMPLATE_JS}
</script>
</body>
</html>"""

    return html
