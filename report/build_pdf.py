# coding:utf-8
"""把 report.md 转成 report.pdf：Markdown -> HTML（python-markdown）-> PDF（Chromium 无头打印）。

用法：python build_pdf.py [chromium 路径]
依赖：pip install markdown；本机需有 Chrome / Chromium。
"""
import os
import re
import shutil
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Noto Serif CJK SC", "Songti SC", "SimSun", "WenQuanYi Zen Hei", serif;
       font-size: 10.5pt; line-height: 1.6; color: #111; }
h1 { font-size: 18pt; text-align: center; margin-bottom: 4pt; }
h2 { font-size: 14pt; border-bottom: 1px solid #999; padding-bottom: 2pt; margin-top: 18pt; }
h3 { font-size: 12pt; margin-top: 12pt; }
table { border-collapse: collapse; margin: 8pt 0; font-size: 9.5pt; width: 100%; }
th, td { border: 1px solid #888; padding: 3pt 6pt; vertical-align: top; }
th { background: #eee; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; background: #f4f4f4; padding: 0 2px; }
pre { background: #f4f4f4; padding: 6pt; font-size: 8.5pt; white-space: pre-wrap; }
pre code { background: none; }
blockquote { border-left: 3px solid #aaa; margin: 6pt 0; padding: 2pt 10pt; color: #444; }
img { display: block; max-width: 100%; max-height: 230mm; margin: 6pt auto; page-break-inside: avoid; }
p:has(> img) { page-break-inside: avoid; }
hr { border: none; border-top: 1px solid #ccc; }
"""


def find_chromium():
    if len(sys.argv) > 1:
        return sys.argv[1]
    for name in ('/opt/pw-browsers/chromium', 'chromium', 'chromium-browser', 'google-chrome',
                 '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
        path = name if os.path.isabs(name) else shutil.which(name)
        if path and os.path.exists(path):
            return path
    sys.exit("找不到 Chromium/Chrome，请把路径作为第一个参数传入")


LIST_RE = re.compile(r'^\s*([*+-]|\d+\.)\s')


def normalize_lists(text):
    """python-markdown 要求嵌套列表缩进 4 空格、列表前有空行；report.md 按 GitHub 习惯写，这里转换一下。"""
    out, in_code = [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
        if not in_code:
            line = re.sub(r'^( +)', lambda m: m.group(1) * 2, line)  # 缩进加倍：2 -> 4
            prev = out[-1] if out else ''
            if LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev):
                out.append('')  # 列表前补空行
        out.append(line)
    return '\n'.join(out)


def main():
    with open(os.path.join(HERE, 'report.md'), encoding='utf-8') as f:
        body = markdown.markdown(normalize_lists(f.read()), extensions=['tables', 'fenced_code'])
    html = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<title>决策树编程作业报告</title><style>%s</style></head><body>%s</body></html>' % (CSS, body))
    html_path = os.path.join(HERE, 'report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    pdf_path = os.path.join(HERE, 'report.pdf')
    subprocess.run([find_chromium(), '--headless', '--no-sandbox', '--disable-gpu',
                    '--no-pdf-header-footer', '--print-to-pdf=' + pdf_path,
                    'file://' + html_path], check=True)
    print('已生成', pdf_path)


if __name__ == '__main__':
    main()
