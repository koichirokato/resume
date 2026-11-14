"""Builds index.html for the resume page from data.py."""

import html
import pathlib
import sys

import data

OUT = pathlib.Path(sys.argv[1])


def esc(s):
    return html.escape(s, quote=True)


def authors(s):
    out = esc(s)
    for name in data.ME:
        out = out.replace(name, f"<span class=\"me\">{name}</span>")
    return out


def doi_link(doi):
    if not doi:
        return ""
    return f' <a class="doi" href="https://doi.org/{esc(doi)}">doi:{esc(doi)}</a>'


def pub_list(items):
    rows = []
    for year, au, title, venue, doi, _ in items:
        rows.append(
                f'<li><span class="year">{year}</span><div>'
                f'<p class="title">{esc(title)}</p>'
                f'<p class="authors">{authors(au)}</p>'
                f'<p class="venue">{esc(venue)}{doi_link(doi)}</p>'
                f"</div></li>")
    return '<ol class="pubs">' + "".join(rows) + "</ol>"


def marks(venue, code):
    labels = data.AWARD_MARKS.get((venue, code), [])
    if not labels:
        return ""
    tags = "".join(f'<li>{esc(label)}</li>' for label in labels)
    return f'<ul class="marks" aria-label="受賞">{tags}</ul>'


def domestic_list():
    rows = []
    for year, venue, code, au, title, _ in data.DOMESTIC:
        name = data.VENUES[venue.rstrip("0123456789")]
        rows.append(
            f'<li><span class="year">{year}</span><div>'
            f'<p class="title">{esc(title)}</p>'
            f'{marks(venue, code)}'
            f'<p class="authors">{authors(au)}</p>'
            f'<p class="venue">{esc(name)} {year}'
            f'{"、講演番号 " + esc(code) if code else ""}</p>'
            f"</div></li>")
    return '<ol class="pubs">' + "".join(rows) + "</ol>"


def awards():
    rows = "".join(
            f'<tr><td class="when">{esc(d)}</td><td><p class="title">{esc(a)}</p>'
            f'<p class="sub">{esc(w)}</p></td><td class="role">{esc(r)}</td></tr>'
            for d, a, w, r in data.AWARDS)
    return f'<table class="awards"><tbody>{rows}</tbody></table>'


def detail(url):
    if not url:
        return ""
    return f' <a class="detail" href="{esc(url)}">概要（PDF）</a>'


def contests():
    rows = "".join(
        f'<tr><td class="when">{esc(d)}</td><td><p class="title">{esc(c)} {esc(a)}</p>'
        f'<p class="sub">{esc(w)}{detail(u)}</p></td><td class="role">{esc(r)}</td></tr>'
        for d, c, a, w, r, u in data.CONTESTS)
    return f'<table class="awards"><tbody>{rows}</tbody></table>'


def sources():
    parts = []
    for group, items in data.SOURCES:
        links = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for t, u in items)
        parts.append(f"<h3>{esc(group)}</h3><ul>{links}</ul>")
    return "".join(parts)



page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>加藤宏一朗 レジュメ</title>
<meta name="description" content="ロボットソフトウェアエンジニア 加藤宏一朗のレジュメ">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+JP:wght@400;500&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>

<header class="masthead">
  <h1>加藤宏一朗</h1>
  <p class="en">Koichiro Kato</p>
  <p class="lede">ロボットソフトウェアエンジニア</p>
  <ul class="links">
    <li><a href="https://github.com/koichirokato">github.com/koichirokato</a></li>
  </ul>
</header>

<section>
  <h2>学歴</h2>
  <div class="school">
    <h3>芝浦工業大学 <span class="alt">Shibaura Institute of Technology</span></h3>
    <p>大学院 理工学研究科 機械工学専攻 修士課程 2022年修了</p>
    <p>知能機械システム研究室（指導教員 松日楽信人 教授）</p>
  </div>
</section>

<section>
  <h2>受賞</h2>
  {awards()}
</section>

<section>
  <h2>コンテスト</h2>
  {contests()}
</section>

<section>
  <h2>論文誌</h2>
  {pub_list(data.JOURNALS)}
</section>

<section>
  <h2>国際会議</h2>
  {pub_list(data.INTERNATIONAL)}
</section>

<section>
  <h2>国内学会</h2>
  {domestic_list()}
</section>

<footer>
  <p>公開されている記録だけをもとに作成しています。2026年11月更新</p>
  <h2 class="sources-title">出典</h2>
  {sources()}
</footer>

</main>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "10b709bac2104dcbbf747a487e776249"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""
OUT.write_text(page, encoding="utf-8")
print("wrote", OUT)
