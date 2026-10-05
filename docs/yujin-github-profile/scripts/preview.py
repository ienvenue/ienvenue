#!/usr/bin/env python3
"""用 GitHub 官方接口渲染 README.md，生成本地预览页。

用法：
    python3 preview.py <主页仓库目录> <输出目录>
    python3 -m http.server 8011 -d <输出目录>   # 然后打开 http://localhost:8011/

需要已登录的 gh 命令行（gh auth status）。
渲染用 mode=markdown（和仓库 README 一致：单个换行不会变成 <br>）。
样式是仿 GitHub 的近似效果，跟随系统深浅色。每次改完 README 要重新运行，刷新页面不会更新。
"""
import shutil
import subprocess
import sys
from pathlib import Path

CSS = """
:root{--fg:#1f2328;--muted:#59636e;--bd:#d1d9e0;--bg:#fff;--code:#818b981f;--link:#0969da}
@media (prefers-color-scheme:dark){:root{--fg:#f0f6fc;--muted:#9198a1;--bd:#3d444d;--bg:#0d1117;--code:#656c7633;--link:#4493f8}}
body{background:var(--bg);color:var(--fg);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;margin:0}
.box{max-width:840px;margin:24px auto;border:1px solid var(--bd);border-radius:6px;padding:32px;box-sizing:border-box}
a{color:var(--link);text-decoration:none}
h1{font-size:2em;border-bottom:1px solid var(--bd);padding-bottom:.3em;margin:.67em 0 16px;font-weight:600}
h2{font-size:1.5em;border-bottom:1px solid var(--bd);padding-bottom:.3em;margin:24px 0 16px;font-weight:600}
h3{font-size:1.25em;margin:24px 0 16px;font-weight:600}
h4{font-size:1em;margin:24px 0 16px;font-weight:600}
p,blockquote,ul,ol,table{margin:0 0 16px}
hr{height:.25em;background:var(--bd);border:0;margin:24px 0}
blockquote{padding:0 1em;color:var(--muted);border-left:.25em solid var(--bd)}
code{background:var(--code);border-radius:6px;padding:.2em .4em;font:85% ui-monospace,SFMono-Regular,Menlo,monospace}
sub{font-size:75%}
img{max-width:100%}
table{border-collapse:collapse}td,th{border:1px solid var(--bd);padding:6px 13px}
@media (max-width:500px){.box{margin:0;border:0;padding:16px}}
"""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    readme = repo / "README.md"
    if not readme.exists():
        sys.exit(f"找不到 {readme}")
    body = subprocess.run(
        ["gh", "api", "markdown", "-f", "mode=markdown", "-F", f"text=@{readme}"],
        check=True, capture_output=True, text=True,
    ).stdout
    out.mkdir(parents=True, exist_ok=True)
    if (repo / "assets").is_dir():
        shutil.copytree(repo / "assets", out / "assets", dirs_exist_ok=True)
    (out / "index.html").write_text(
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>README 预览</title><style>{CSS}</style></head>"
        f'<body><div class="box">{body}</div></body></html>',
        encoding="utf-8",
    )
    print(f"已生成 {out / 'index.html'}")
    print(f"预览：python3 -m http.server 8011 -d {out}")


if __name__ == "__main__":
    main()
