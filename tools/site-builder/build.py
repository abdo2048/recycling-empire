#!/usr/bin/env python3
"""Recycling Empire site builder — renders materials/ into docs/ (PLAYBOOK Phase 6).

Plain markdown stays the source of truth; this script only presents it.
- One home page with a card per material (from material.yaml)
- Per-material dashboard, ranking, methods, registry, inventions, reports,
  research shelf, sources index + per-source pages, charter, glossary, state, log
- Link rewriting: migrated .md links become site pages; heavy originals become
  links into the butt-lab archive
- Evidence-label chips, status badges, client-side search index
- No frameworks: Python stdlib + markdown + PyYAML

Usage: python3 tools/site-builder/build.py [repo_root]   (default: repo of this file)
"""
import json
import os
import posixpath
import re
import shutil
import sys
from string import Template

try:
    import markdown
except ImportError:
    sys.exit("pip install markdown")
try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", ".."))
DOCS = os.path.join(REPO, "docs")
DOCS_SRC = REPO

ARCHIVE_RAW = "https://raw.githubusercontent.com/abdo2048/butt-lab/main/"
ARCHIVE_BLOB = "https://github.com/abdo2048/butt-lab/blob/main/"
ARCHIVE_TREE = "https://github.com/abdo2048/butt-lab/tree/main/"

MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "sane_lists"],
    extension_configs={"toc": {"permalink": False}},
)

# ---------------------------------------------------------------- utilities

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def strip_angle_links(text):
    """[label](<path>) -> [label](path)  (angle-bracket destinations)."""
    return re.sub(r"\]\(<([^)>]+)>\)", r"](\1)", text)


def strip_tags(html):
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def parse_meta_block(text):
    """Parse a YAML frontmatter block or the fenced metadata block that follows
    the H1 (butt-lab convention: 'the site builder reads it')."""
    m = re.search(r"^---\n(.*?)\n---\n", text, re.S)
    if m and yaml:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
            return meta, text[m.end():]
        except Exception:
            pass
    m = re.search(r"^# .+?\n+```[^\n]*\n(.*?)\n```\n", text, re.S)
    if m:
        meta = {}
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip().strip('"')
            if v.startswith("[") and v.endswith("]"):
                meta[k] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            else:
                meta[k] = v
        body = text[:m.start()] + text[m.end():]
        body = re.sub(r"^\(Keep the block above[^)]*\)\s*\n", "", body)
        return meta, body
    return {}, text


def h1_of(text, fallback):
    m = re.match(r"^# (.+?)\s*$", text, re.M)
    return m.group(1) if m else fallback


def chip(m):
    lab = m.group(1)
    return f'<span class="chip chip-{lab}">{lab.replace("_", " ")}</span>'


def render_md(text):
    MD.reset()
    html = MD.convert(text)
    html = re.sub(r"<code>(source_supported|ai_inference|ai_proposal|parameter_not_located)</code>", chip, html)
    return html, MD.toc_tokens


def toc_html(tokens):
    items = []
    for t in tokens:
        items.append(f'<a href="#{t["id"]}">{esc(t["name"])}</a>')
        for c in t.get("children", []):
            items.append(f'<a class="lvl3" href="#{c["id"]}">{esc(c["name"])}</a>')
    if not items:
        return ""
    return '<nav class="toc" aria-label="On this page"><h2>On this page</h2>' + "\n".join(items) + "</nav>"


def md_table_rows(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s\-|]+\|$", line):
            rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def section(text, title_prefix):
    m = re.search(r"^## " + re.escape(title_prefix) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def url_for(from_doc, to_doc):
    return posixpath.relpath(to_doc, posixpath.dirname(from_doc))


def badge(status):
    s = str(status or "").strip()
    if not s:
        return ""
    tone = {"proposed": "b-blue", "draft": "b-amber", "pending_deep_dive": "b-slate",
            "primary-source-read": "b-green", "experimentally-supported-in-source": "b-green"}.get(s, "b-slate")
    return f'<span class="badge {tone}">{esc(s.replace("_", " "))}</span>'


def spec_sheet(meta):
    rows = []
    for k, v in (meta or {}).items():
        if isinstance(v, list):
            v = ", ".join(str(x) for x in v)
        rows.append(f'<div class="spec"><span>{esc(str(k).replace("_", " "))}</span><b>{esc(str(v))}</b></div>')
    return f'<section class="specsheet">{"".join(rows)}</section>' if rows else ""


def pager_html(prev, nxt):
    p = f'<a class="pg prev" href="{prev[1]}"><span>Previous</span><b>{esc(prev[0])}</b></a>' if prev else '<span></span>'
    n = f'<a class="pg next" href="{nxt[1]}"><span>Next</span><b>{esc(nxt[0])}</b></a>' if nxt else '<span></span>'
    return f'<nav class="pager">{p}{n}</nav>'


SEARCH = []
PAGES = []
MATS = []


class Material:
    def __init__(self, folder):
        self.folder = folder
        self.abs = os.path.join(DOCS_SRC, folder.replace("/", os.sep))
        self.slug = posixpath.basename(folder)
        cfg = {}
        p = os.path.join(self.abs, "material.yaml")
        if os.path.exists(p) and yaml:
            try:
                cfg = yaml.safe_load(read(p)) or {}
            except Exception:
                cfg = {}
        self.cfg = cfg
        self.name = cfg.get("name") or self.slug.replace("-", " ").title()
        self.pages = {}

    def has(self, rel):
        return os.path.exists(os.path.join(self.abs, rel.replace("/", os.sep)))

    def resolve(self, href, src_rel):
        if re.match(r"^(https?:|mailto:|#)", href):
            return None
        if href.startswith("/"):
            rel = posixpath.normpath(href[1:])
        else:
            rel = posixpath.normpath(posixpath.join(posixpath.dirname(src_rel), href))
        if rel.startswith(".."):
            return None
        if self.has(rel):
            page = self.pages.get(rel)
            if page:
                return ("page", page)
            return ("url", ARCHIVE_RAW + rel)
        ext = posixpath.splitext(rel)[1].lower()
        if ext == ".md":
            return ("url", ARCHIVE_RAW + rel)
        if ext:
            return ("url", ARCHIVE_BLOB + rel)
        return ("url", ARCHIVE_TREE + rel)

    def rewrite_links(self, html, src_rel, from_doc):
        def sub(m):
            attrs, href = m.group(1), m.group(2)
            r = self.resolve(href, src_rel)
            if r is None:
                href2 = href
            elif r[0] == "page":
                href2 = url_for(from_doc, r[1])
            else:
                href2 = r[1]
            return f'<a{attrs}href="{esc(href2)}"'
        return re.sub(r'<a([^>]*)href="([^"]+)"', sub, html)


def article(out_rel, mat, src_rel, title=None, kicker=None, pager=None, sub=None):
    body_md = read(os.path.join((mat.abs if mat else DOCS_SRC), src_rel.replace("/", os.sep)))
    meta = {}
    if mat:
        meta, body_md = parse_meta_block(body_md)
    title = title or h1_of(body_md, posixpath.basename(src_rel))
    body_html, toks = render_md(strip_angle_links(body_md))
    if mat:
        body_html = mat.rewrite_links(body_html, src_rel, out_rel)
    SEARCH.append({"u": out_rel, "t": title, "s": sub or "", "x": strip_tags(body_html)[:1500]})
    return out_rel, {"title": title, "kicker": kicker, "body": body_html,
                     "toc": toc_html(toks), "pager": pager or "", "meta_html": spec_sheet(meta)}


# ---------------------------------------------------------------- material build

def build_material(mat):
    A = mat.abs
    base = mat.folder
    pages = []

    # ---- page map (register before rendering so links resolve)
    for f in sorted(os.listdir(A)):
        if os.path.isfile(os.path.join(A, f)) and f.endswith(".md") and f not in ("STATE.md", "LOG.md", "README.md", "MIGRATION-NOTE.md"):
            mat.pages[f] = f"{base}/{f[:-3]}.html"
    for d, outd in (("methods", "methods"), ("inventions", "inventions"), ("reports/final", "reports"), ("sources", "sources"), ("registry", "registry")):
        dp = os.path.join(A, d.replace("/", os.sep))
        if not os.path.isdir(dp):
            continue
        for f in sorted(os.listdir(dp)):
            rel = f"{d}/{f}"
            if f.endswith(".md") and f != "_cards.md" and f != "README.md":
                mat.pages[rel] = f"{base}/{outd}/{f[:-3]}.html"
            if f == "_cards.md":
                mat.pages[rel] = f"{base}/methods/cards.html"
    rp = os.path.join(A, "methods", "research")
    if os.path.isdir(rp):
        for root, dirs, files in os.walk(rp):
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(root, f), A).replace(os.sep, "/")
                if f.endswith(".md"):
                    mat.pages[rel] = f"{base}/{rel[:-3]}.html"
                elif f.endswith(".csv"):
                    mat.pages[rel] = f"{base}/{rel[:-4]}.html"
    if os.path.isdir(os.path.join(A, "sources")):
        for root, dirs, files in os.walk(os.path.join(A, "sources")):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), A).replace(os.sep, "/")
                if f == "SOURCE.md":
                    sid = posixpath.dirname(rel).split("/")[1]
                    mat.pages[rel] = f"{base}/sources/{sid}.html"
                if f == "INDEX.md":
                    mat.pages["sources/INDEX.md"] = f"{base}/sources/index.html"
                if f == "README.md" and rel.count("/") == 1:
                    mat.pages[rel] = f"{base}/sources/readme.html"
    if mat.has("MIGRATION-NOTE.md"):
        mat.pages["MIGRATION-NOTE.md"] = f"{base}/migration-note.html"

    # ---- data
    counts = {}
    mdir = os.path.join(A, "methods")
    counts["methods"] = len([f for f in os.listdir(mdir) if re.match(r"M-\d", f)]) if os.path.isdir(mdir) else 0
    idir = os.path.join(A, "inventions")
    counts["inventions"] = len([f for f in os.listdir(idir) if f.startswith("INV-")]) if os.path.isdir(idir) else 0
    sdir = os.path.join(A, "sources")
    idx_ids = []
    if mat.has("sources/INDEX.md"):
        idx_ids = re.findall(r"^\| `([^`]+)`", read(os.path.join(A, "sources", "INDEX.md")), re.M)
    counts["sources"] = len(idx_ids) if idx_ids else (len([d for d in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, d))]) if os.path.isdir(sdir) else 0)
    cards_meta = parse_meta_block(read(os.path.join(mdir, "_cards.md")))[0] if os.path.exists(os.path.join(mdir, "_cards.md")) else {}
    counts["cards"] = cards_meta.get("count", "")
    reg_entries = []
    if yaml and mat.has("registry/methods.yaml"):
        try:
            reg_entries = (yaml.safe_load(read(os.path.join(A, "registry", "methods.yaml"))) or {}).get("entries", [])
        except Exception:
            reg_entries = []
    counts["registry"] = len(reg_entries)
    mat.counts = dict(counts)

    ranking_md = read(os.path.join(A, "ranking.md")) if mat.has("ranking.md") else ""
    tableA = []
    if ranking_md:
        rows = md_table_rows(section(ranking_md, "Table A"))[1:]
        for r in rows:
            if len(r) >= 10:
                tableA.append({"rank": r[0], "name": r[1], "total": r[8], "note": r[9]})
    test_first = []
    if ranking_md:
        for line in section(ranking_md, "Test first").splitlines():
            m = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
            if m:
                test_first.append(m.group(2))

    state_md = read(os.path.join(A, "STATE.md")) if mat.has("STATE.md") else ""
    inflight = ""
    hdr = {}
    if state_md:
        m = re.search(r"^## In flight right now\n(.+?)(?=\n## |\Z)", state_md, re.S)
        if m:
            inflight = m.group(1).strip().splitlines()[0]
        m = re.search(r"^Updated: (.+?) \| Phase: (.+?) \| Version: (.+?)$", state_md, re.M)
        if m:
            hdr = {"updated": m.group(1), "phase": m.group(2), "version": m.group(3)}
    version = mat.cfg.get("version") or hdr.get("version", "")

    # ================= dashboard =================
    stop = mat.cfg.get("stop_conditions") or []
    banner = f'<div class="gate"><b>Stop-condition</b> {esc(str(stop[0]))}</div>' if stop else ""

    journey = []
    if ranking_md:
        journey.append(("1", "Ranking — the verdict", "Six-factor scores for every route, the test-first list, and why the metals gate shapes the top of the table.", "ranking.html", "short read"))
    if mat.has("reports/final/batch-01-synthesis.md"):
        journey.append(("2", "Final reports", "The evidence boundary in full prose: what the desk investigation established and what it did not.", "reports/index.html", "deep read"))
    if counts["methods"]:
        journey.append(("3", "Action plans M-01…M-08", "Each priority method as an executable protocol: disclosed steps, labeled gap-fills, safety notes, lab checks.", "methods/index.html", "deep reads"))
    if counts["inventions"]:
        journey.append(("4", "The invention", "The invented route that turns the field's missing mass balances into the deliverable, with a falsifier ledger.", "inventions/index.html", "deep read"))
    if counts["sources"]:
        journey.append(("5", "Sources shelf", "Every document behind the claims: metadata pages, archive originals, AI-readable conversions.", "sources/index.html", "reference"))
    journey.append(("6", "Charter, glossary, state & log", "The rules the research obeys, the vocabulary, and the full session record.", "charter.html", "reference"))

    jcards = "".join(f'<a class="jcard" href="{u}"><span class="jn">{n}</span><b>{esc(t)}</b><p>{esc(d)}</p><span class="jl">{l}</span></a>'
                     for n, t, d, u, l in journey)

    stat = ('<div class="stats">' +
            f'<div class="stat"><b>{counts["sources"]}</b><span>sources</span></div>'
            f'<div class="stat"><b>{counts["registry"]}</b><span>registry entries</span></div>'
            f'<div class="stat"><b>{counts["methods"]}</b><span>action plans</span></div>'
            f'<div class="stat"><b>{counts["inventions"]}</b><span>invention</span></div>'
            f'<div class="stat"><b>{counts["cards"]}</b><span>summary cards</span></div></div>')

    snap = ""
    if tableA:
        rows = "".join(f'<tr><td class="rk">{esc(t["rank"])}</td><td><a href="methods/index.html">{esc(t["name"])}</a></td>'
                       f'<td class="tot">{esc(t["total"])}</td><td class="note">{esc(t["note"][:150])}</td></tr>' for t in tableA[:3])
        snap = (f'<section class="panel"><h2>Ranking snapshot</h2><table class="tbl"><thead><tr><th>#</th><th>Route</th><th>Total</th><th>Why</th></tr></thead>'
                f'<tbody>{rows}</tbody></table><p class="more"><a href="ranking.html">Full six-factor table, all 36 items, rubrics and the test-first list →</a></p></section>')

    tprev = ""
    if test_first:
        items = "".join(f"<li>{esc(t[:220])}</li>" for t in test_first[:3])
        tprev = f'<section class="panel"><h2>Test first</h2><ol>{items}</ol><p class="more"><a href="ranking.html">The complete ordered test list →</a></p></section>'

    phases = ["0 Setup", "1 Sources", "2 Registry", "3 Plans", "4 Invention", "5 Ranking", "6 Site", "7 Review"]
    phase_no = 7 if (tableA and counts["methods"]) else 6
    pstrip = '<ol class="phases">' + "".join(f'<li class="{"done" if i < phase_no else ("now" if i == phase_no else "")}">{p}</li>' for i, p in enumerate(phases)) + "</ol>"

    mig = ""
    if mat.has("MIGRATION-NOTE.md"):
        mig = '<p class="more"><a href="migration-note.html">Migration note — what moved here, what stayed in the butt-lab archive →</a></p>'

    prio = mat.cfg.get("priority_methods") or []
    prio_html = '<p class="prio"><b>Priority methods:</b> ' + ", ".join(f"<code>{esc(str(p))}</code>" for p in prio) + "</p>" if prio else ""

    dash_body = f"""{banner}
<div class="idcard">
  <div class="idrow"><span>Version</span><b>{esc(str(version))}</b></div>
  <div class="idrow"><span>Phase</span><b>{esc(str(hdr.get('phase', '')))}</b></div>
  <div class="idrow"><span>Updated</span><b>{esc(str(hdr.get('updated', '')))}</b></div>
  <div class="idrow"><span>Status</span><b>{esc(str(mat.cfg.get('status', 'active')))}</b></div>
</div>
{prio_html}
<div class="panel"><h2>Start here</h2><div class="jgrid">{jcards}</div></div>
{stat}
{snap}
{tprev}
<section class="panel"><h2>Where the project stands</h2><p>{esc(inflight)}</p>{pstrip}</section>
{mig}"""
    SEARCH.append({"u": f"{base}/index.html", "t": f"{mat.name} — material dashboard", "s": "", "x": strip_tags(dash_body)[:1200]})
    pages.append((f"{base}/index.html", {"title": f"{mat.name} — material dashboard", "kicker": "Material", "body": dash_body}))

    # ================= ranking =================
    if ranking_md:
        pages.append(article(f"{base}/ranking.html", mat, "ranking.md",
                             title="Ranking — six factors, 36 items", kicker="Phase 5 output", sub="ranking"))

    # ================= registry =================
    if reg_entries:
        cards = []
        yhref = ("https://github.com/abdo2048/recycling-empire/blob/main/" + base + "/registry/methods.yaml") \
            if mat.has("registry/methods.yaml") else (ARCHIVE_RAW + "registry/methods.yaml")
        for e in reg_entries:
            rows = []
            for k in ("source_type", "assignee", "mechanism_class", "disclosed", "equipment", "outputs", "gaps", "legal_status", "citations"):
                v = e.get(k)
                if not v:
                    continue
                if isinstance(v, list):
                    v = "; ".join(str(x) for x in v)
                rows.append(f'<div class="spec"><span>{esc(k.replace("_", " "))}</span><b>{esc(str(v))}</b></div>')
            pat = e.get("patents")
            pat_html = '<div class="pats">' + "".join(f"<code>{esc(str(x))}</code>" for x in pat) + "</div>" if pat else ""
            cards.append(f'<article class="regcard"><header><h3><code>{esc(str(e.get("id","")))}</code> {esc(str(e.get("name","")))}</h3>{badge(e.get("status"))}</header>{pat_html}<div class="specsheet">{"".join(rows)}</div></article>')
        pages.append((f"{base}/registry.html", {"title": "Method registry", "kicker": "Phase 2", "body":
            f'<p class="lede">{len(reg_entries)} registered methods — one append-only entry per known method (patented, published, hypothesized, failed). Canonical machine-readable file: <a href="{yhref}">registry/methods.yaml</a>.</p>' + "".join(cards)}))

    # ================= methods =================
    mfiles = sorted([f for f in os.listdir(mdir) if re.match(r"M-\d.*\.md$", f)]) if os.path.isdir(mdir) else []
    mets = []
    for f in mfiles:
        meta, _ = parse_meta_block(read(os.path.join(mdir, f)))
        mets.append({"f": f, "id": meta.get("id", f[:-3]), "name": meta.get("name", ""),
                     "family": meta.get("family", ""), "status": meta.get("status", ""),
                     "version": meta.get("version", ""), "page": mat.pages["methods/" + f]})
    if mets:
        cards = []
        for m in mets:
            rank = next((t["rank"] for t in tableA if str(t["name"]).startswith(str(m["id"]))), "")
            rk = f'<span class="rank">#{esc(rank)}</span>' if rank else ""
            cards.append(f'<a class="mcard" href="{url_for(base + "/methods/index.html", m["page"])}">{rk}<header><h3><code>{esc(str(m["id"]))}</code> {esc(str(m["name"]))}</h3>{badge(m["status"])}</header><span class="mfam">{esc(str(m["family"]))} · {esc(str(m["version"]))}</span></a>')
        cardspage = mat.pages.get("methods/_cards.md", f"{base}/methods/cards.html")
        pages.append((f"{base}/methods/index.html", {"title": "Action plans", "kicker": "Phase 3", "body":
            f'<p class="lede">{len(mets)} priority methods with full action plans; everything else is a summary card in <a href="{url_for(base + "/methods/index.html", cardspage)}">_cards.md</a>. Registry order below; the ranking says which to test first.</p>' + "".join(cards)}))
        for i, m in enumerate(mets):
            prev = (mets[i - 1]["id"], url_for(m["page"], mets[i - 1]["page"])) if i else None
            nxt = (mets[i + 1]["id"], url_for(m["page"], mets[i + 1]["page"])) if i < len(mets) - 1 else None
            pages.append(article(m["page"], mat, "methods/" + m["f"], title=f'{m["id"]} — {m["name"]}',
                                 kicker="Action plan", pager=pager_html(prev, nxt), sub="methods"))
        pages.append(article(cardspage, mat, "methods/_cards.md", title="Registry summary cards", kicker="Phase 3b", sub="methods"))

    # ================= inventions =================
    idir = os.path.join(A, "inventions")
    if os.path.isdir(idir):
        invs = sorted([f for f in os.listdir(idir) if f.endswith(".md") and f != "TEMPLATE.md"])
        cards = []
        for f in invs:
            meta, _ = parse_meta_block(read(os.path.join(idir, f)))
            t = h1_of(read(os.path.join(idir, f)), f[:-3])
            href = url_for(base + "/inventions/index.html", mat.pages["inventions/" + f])
            hero = ' <span class="badge b-green">the invention</span>' if f.startswith("INV-") else ""
            cards.append(f'<a class="mcard" href="{href}"><header><h3>{esc(t)}</h3>{badge(meta.get("status"))}{hero}</header></a>')
        pages.append((f"{base}/inventions/index.html", {"title": "Inventions", "kicker": "Phase 4", "body":
            '<p class="lede">The AI\'s own method designs — built from the gathered knowledge, every assumption labeled, falsifiers attached. An invention is not a claim of novelty or patentability.</p>' + "".join(cards)}))
        for f in invs:
            t = h1_of(read(os.path.join(idir, f)), f[:-3])
            pages.append(article(mat.pages["inventions/" + f], mat, "inventions/" + f, title=t, kicker="Invention", sub="inventions"))

    # ================= reports =================
    rf = os.path.join(A, "reports", "final")
    if os.path.isdir(rf):
        reps = sorted(f for f in os.listdir(rf) if f.endswith(".md"))
        cards = "".join(f'<a class="mcard" href="{url_for(base + "/reports/index.html", mat.pages["reports/final/" + f])}"><header><h3>{esc(h1_of(read(os.path.join(rf, f)), f))}</h3></header></a>' for f in reps)
        pages.append((f"{base}/reports/index.html", {"title": "Final reports", "kicker": "Desk synthesis", "body":
            '<p class="lede">The batch-01 desk synthesis and its validation record — the evidence boundary in full prose.</p>' + cards}))
        for f in reps:
            t = h1_of(read(os.path.join(rf, f)), f)
            pages.append(article(mat.pages["reports/final/" + f], mat, "reports/final/" + f, title=t, kicker="Report", sub="reports"))

    # ================= research shelf =================
    rp = os.path.join(A, "methods", "research")
    if os.path.isdir(rp):
        entries = []
        for root, dirs, files in os.walk(rp):
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(root, f), A).replace(os.sep, "/")
                if not f.endswith((".md", ".csv")):
                    continue
                page = mat.pages[rel]
                t = h1_of(read(os.path.join(root, f)), f) if f.endswith(".md") else f[:-4] + " (data table)"
                kind = "Findings" if "FINDINGS" in f else ("Transcript" if "transcripts/" in rel else ("Data" if f.endswith(".csv") else "Note"))
                entries.append((rel, t, kind, page))
        cards = "".join(f'<a class="mcard" href="{url_for(base + "/research/index.html", pg)}"><header><h3>{esc(t)}</h3><span class="mfam">{k}</span></header></a>' for _, t, k, pg in entries)
        pages.append((f"{base}/research/index.html", {"title": "Research shelf", "kicker": "Arena + data", "body":
            '<p class="lede">Multi-agent arena research on the remaining wishes (mass figures, trade-secret search): findings, transcripts and data tables. Raw fetch artifacts (attempts/, cdx/) stay in the butt-lab archive.</p>' + cards}))
        for rel, t, kind, pg in entries:
            if rel.endswith(".csv"):
                lines = [line.split(",") for line in read(os.path.join(A, rel.replace("/", os.sep))).strip().splitlines()]
                head, rows = lines[0], lines[1:]
                trs = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
                body = '<table class="tbl"><thead><tr>' + "".join(f"<th>{esc(c)}</th>" for c in head) + f"</tr></thead><tbody>{trs}</tbody></table>"
                SEARCH.append({"u": pg, "t": t, "s": "research", "x": strip_tags(body)[:800]})
                pages.append((pg, {"title": t, "kicker": "Research data", "body": body}))
            else:
                pages.append(article(pg, mat, rel, kicker=kind, sub="research"))

    # ================= sources =================
    if os.path.isdir(sdir):
        idx_rows = {}
        if mat.has("sources/INDEX.md"):
            for r in md_table_rows(read(os.path.join(A, "sources", "INDEX.md")))[1:]:
                if len(r) < 4:
                    continue
                idm = re.match(r"`([^`]+)`", r[0])
                if not idm:
                    continue
                om = re.search(r"\[\s*([\d.]+\s*[KMG]B)\s*\]", r[1])
                idx_rows[idm.group(1)] = {"fig": r[3].strip(), "size": om.group(1) if om else "", "text": r[2].strip() != "—"}
        srows = []
        local_dirs = [d for d in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, d))]
        for sid in sorted(set(list(idx_rows.keys()) + local_dirs)):
            info = idx_rows.get(sid, {})
            title, stype = sid, ""
            smd = os.path.join(sdir, sid, "SOURCE.md")
            has_src = os.path.exists(smd)
            if has_src:
                txt = read(smd)
                m = re.search(r"^## Exact title\s*\n(.+?)$", txt, re.M)
                if m:
                    title = m.group(1).strip()
                m = re.search(r"^## Type\s*\n(.+?)$", txt, re.M)
                if m:
                    stype = m.group(1).strip()[:60]
            srows.append({"id": sid, "title": title, "type": stype, "fig": info.get("fig", ""),
                          "size": info.get("size", ""), "text": info.get("text", False), "src": has_src})
        trs = ""
        for r in srows:
            sid = r["id"]
            det = mat.pages.get(f"sources/{sid}/SOURCE.md")
            if det:
                idcell = f'<a href="{url_for(base + "/sources/index.html", det)}">{esc(sid)}</a>'
                meta_cell = '<span class="badge b-green">metadata</span>'
            else:
                idcell = f'<a href="{ARCHIVE_TREE}sources/{sid}/" rel="noopener">{esc(sid)} ↗</a>'
                meta_cell = '<span class="badge b-slate">index only</span>'
            trs += (f'<tr><td>{idcell}</td><td>{esc(r["title"][:90])}</td><td>{meta_cell}</td>'
                    f'<td class="num">{esc(r["fig"] or "—")}</td><td class="num">{esc(r["size"] or "—")}</td>'
                    f'<td>{("yes" if r["text"] else "—")}</td></tr>')
        srcs_grid = (f'<p class="lede">{len(srows)} documents, one folder each. Heavy originals and the AI-readable text.md conversions '
                     f'live in the frozen <a href="{ARCHIVE_TREE}sources/" rel="noopener">butt-lab archive ↗</a>. '
                     f'Rows with a metadata page link to it; the rest link straight to their archive folder. '
                     f'Filter below, or scroll the canonical <code>sources/INDEX.md</code> table.</p>'
                     f'<input id="srcfilter" type="search" placeholder="Filter sources…" autocomplete="off">'
                     f'<table class="tbl" id="srctable"><thead><tr><th>Source</th><th>Title</th><th>Metadata</th><th>Figs</th><th>Size</th><th>AI text</th></tr></thead><tbody>{trs}</tbody></table>')
        idx_out = f"{base}/sources/index.html"
        idx_out, idx_out_d = article(idx_out, mat, "sources/INDEX.md", title="Sources — the document shelf", kicker="Phase 1", sub="sources")
        idx_out_d["body"] = srcs_grid + '<section class="panel"><h2>Canonical index (sources/INDEX.md)</h2>' + idx_out_d["body"] + "</section>"
        pages.append((idx_out, idx_out_d))
        if mat.has("sources/README.md"):
            pages.append(article(f"{base}/sources/readme.html", mat, "sources/README.md",
                                 title="The two-reader rule (sources/README.md)", kicker="How the shelf works", sub="sources"))
        for r in srows:
            sid = r["id"]
            det = mat.pages.get(f"sources/{sid}/SOURCE.md")
            orig = f"{ARCHIVE_TREE}sources/{sid}/"
            if det:
                d = article(det, mat, f"sources/{sid}/SOURCE.md", title=r["title"], kicker="Source", sub="sources")[1]
                note = (f'<div class="callout">Full document in the butt-lab archive: <a href="{orig}" rel="noopener">sources/{esc(sid)}/ ↗</a> · '
                        f'<a href="{ARCHIVE_RAW}sources/{sid}/text.md" rel="noopener">text.md ↗</a></div>')
                d["body"] = note + d["body"]
                pages.append((det, d))

    # ================= charter / glossary / state / log / migration =================
    for rel, out, t, k in [("charter.md", "charter.html", "Research charter", "Rules"),
                           ("GLOSSARY.md", "glossary.html", "Glossary", "Vocabulary"),
                           ("MIGRATION-NOTE.md", "migration-note.html", "Migration note", "Phase 6")]:
        if mat.has(rel):
            pages.append(article(f"{base}/{out}", mat, rel, title=t, kicker=k))
    if state_md:
        html, toks = render_md(strip_angle_links(state_md))
        html = mat.rewrite_links(html, "STATE.md", f"{base}/state.html")
        SEARCH.append({"u": f"{base}/state.html", "t": "STATE.md — resume file", "s": "", "x": strip_tags(html)[:1500]})
        pages.append((f"{base}/state.html", {"title": "STATE.md", "kicker": "Resume file", "body": html, "toc": toc_html(toks)}))
    if mat.has("LOG.md"):
        pages.append(article(f"{base}/log.html", mat, "LOG.md", title="LOG.md — session log", kicker="Append-only record"))
    return pages


# ---------------------------------------------------------------- shell

BASE_T = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title — Recycling Empire</title>
<meta name="doc-root" content="$root">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="$root/assets/style.css">
</head>
<body data-root="$root">
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <nav class="topnav" aria-label="Primary">
    <a class="brand" href="${root}index.html">Recycling<em>Empire</em></a>
    <a href="${root}index.html#materials">Materials</a>
    <a href="${root}playbook.html">Playbook</a>
    <a href="${root}site-design.html">Site design</a>
    <button id="searchbtn" type="button" aria-label="Search">Search <kbd>Ctrl K</kbd></button>
  </nav>
</header>
$crumbs
<main id="main">
$sidebar
<article class="content">
  $h1block
  $meta_html
  $body
  $pager
</article>
$toc
</main>
<footer>
  <div class="legend">
    <span class="chip chip-source_supported">source supported</span>
    <span class="chip chip-ai_inference">ai inference</span>
    <span class="chip chip-ai_proposal">ai proposal</span>
    <span class="chip chip-parameter_not_located">parameter not located</span>
  </div>
  <p>Desk research only — no physical trials, no clean/safe/validated claims. Stop-conditions bind all product-facing work. Built by the <a href="${root}playbook.html">Recycling Empire playbook</a>; markdown is the source of truth.</p>
  <p><a href="https://github.com/abdo2048/recycling-empire" rel="noopener">GitHub</a> · <a href="https://github.com/abdo2048/butt-lab" rel="noopener">butt-lab archive</a> · <a href="${root}site-design.html">Design</a></p>
</footer>
<div class="soverlay" id="soverlay" hidden>
  <div class="sbox">
    <input id="sinput" type="search" placeholder="Search the knowledge base…" autocomplete="off">
    <div id="sresults" class="sresults"></div>
    <p class="shint">Esc to close · results come from the built index</p>
  </div>
</div>
<script src="$root/assets/site.js" defer></script>
</body>
</html>
""")

SECTIONS = [("index.html", "Overview"), ("ranking.html", "Ranking"), ("methods/index.html", "Action plans"),
            ("methods/cards.html", "Summary cards"), ("registry.html", "Registry"), ("inventions/index.html", "Inventions"),
            ("reports/index.html", "Final reports"), ("sources/index.html", "Sources"), ("research/index.html", "Research shelf"),
            ("charter.html", "Charter"), ("glossary.html", "Glossary"), ("state.html", "State"), ("log.html", "Log"),
            ("migration-note.html", "Migration note")]


def write_page(docpath, data, mat):
    full = os.path.join(DOCS, docpath.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    depth = docpath.count("/")
    root = "./" if depth == 0 else "../" * depth
    if docpath == "index.html":
        cb = '<nav class="crumbs" aria-label="Breadcrumb"><ol><li aria-current="page">Recycling Empire</li></ol></nav>'
    else:
        items = [('<a href="' + root + 'index.html">Home</a>', )]
        parts = []
        items = [f'<li><a href="{root}index.html">Home</a></li>']
        if mat:
            items.append(f'<li><a href="{root}index.html#materials">Materials</a></li>')
            if not docpath.endswith("index.html") or docpath.count("/") > 1:
                pass
            items.append(f'<li aria-current="page">{esc(data["title"])}</li>')
        else:
            items.append(f'<li aria-current="page">{esc(data["title"])}</li>')
        cb = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(items) + '</ol></nav>'
    all_paths = {p for p, _ in PAGES}
    if mat:
        nav = []
        for rel, label in SECTIONS:
            pg = f"{mat.folder}/{rel}"
            if pg in all_paths:
                cls = ' class="on"' if docpath == pg else ""
                nav.append(f'<a{cls} href="{url_for(docpath, pg)}">{label}</a>')
        sidebar = f'<aside class="side" aria-label="Material sections"><h2>{esc(mat.name)}</h2><nav>{"".join(nav)}</nav></aside>'
    else:
        sidebar = ""
    mat_name = mat and docpath or None
    h1block = ""
    if not data.get("notitle"):
        h1block = (f'<p class="kicker">{esc(data["kicker"])}</p>' if data.get("kicker") else "") + f"<h1>{esc(data['title'])}</h1>"
    body = BASE_T.substitute(
        title=esc(data["title"]), root=root, crumbs=cb, sidebar=sidebar,
        h1block=h1block,
        meta_html=data.get("meta_html", ""), body=data["body"], toc=data.get("toc", ""), pager=data.get("pager", ""))
    with open(full, "w", encoding="utf-8") as f:
        f.write(body)


def build_home():
    cards = ""
    for m in MATS:
        c = getattr(m, "counts", {})
        blurb = (f"{c.get('sources', '—')} sourced documents, {c.get('registry', '—')} registered methods, "
                 f"{c.get('methods', '—')} action plans, {c.get('inventions', '—')} invented route(s)")
        if m.slug == "cigarette-butts":
            blurb += " — under the Gap-fill labeling system and the metals stop-condition (Cd/Pb/As/Hg)."
        cards += (f'<a class="matcard" href="{m.folder}/index.html"><h3>{esc(m.name)}</h3><p>{esc(blurb)}</p>'
                  f'<span class="mv">{esc(str(m.cfg.get("version", "")))}</span></a>')
    hero = f"""<section class="hero">
<h1>Waste materials, turned into <em>verifiable</em> knowledge bases.</h1>
<p>Every material gets sources, method action plans, invented routes, and a six-factor ranking —
built by an AI under strict labeling rules, reviewed by humans and other AIs, and written so a
real team can test it in qualified labs.</p>
<p class="cta"><a class="btn" href="#materials">Browse materials</a>
<a class="btn ghost" href="playbook.html">Read the playbook</a></p>
</section>
<section id="materials"><h2 class="sr">Materials</h2><div class="mgrid">{cards}</div></section>"""
    SEARCH.append({"u": "index.html", "t": "Recycling Empire — home", "s": "", "x": strip_tags(hero)[:600]})
    write_page("index.html", {"title": "Recycling Empire", "kicker": "", "body": hero, "notitle": True}, None)


def main():
    global DOCS_SRC
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)
    DOCS_SRC = REPO

    for src, out in [("PLAYBOOK.md", "playbook.html"), ("SITE-DESIGN.md", "site-design.html"),
                     ("START-A-NEW-MATERIAL.md", "start-a-new-material.html")]:
        d = article(out, None, src, kicker="System")[1]
        root_pages = {p for p, _ in PAGES} | {"start-a-new-material.html"}

        def sub_root(m, _src=src):
            attrs, href = m.group(1), m.group(2)
            if href.startswith(("http", "#", "mailto:")):
                return m.group(0)
            if href in ("PLAYBOOK.md",):
                href2 = "playbook.html"
            elif href in ("SITE-DESIGN.md",):
                href2 = "site-design.html"
            elif href in ("START-A-NEW-MATERIAL.md",):
                href2 = "start-a-new-material.html"
            elif os.path.exists(os.path.join(REPO, href.replace("/", os.sep))):
                href2 = "https://github.com/abdo2048/recycling-empire/blob/main/" + href
            else:
                return m.group(0)
            return f'<a{attrs}href="{esc(href2)}"'

        d["body"] = re.sub(r'<a([^>]*)href="([^"]+)"', sub_root, d["body"])
        PAGES.append((out, d))

    mroot = os.path.join(REPO, "materials")
    if os.path.isdir(mroot):
        for slug in sorted(os.listdir(mroot)):
            if os.path.exists(os.path.join(mroot, slug, "material.yaml")):
                mat = Material(f"materials/{slug}")
                MATS.append(mat)
                PAGES.extend(build_material(mat))

    for docpath, data in PAGES:
        if docpath == "index.html":
            continue
        mat = next((m for m in MATS if docpath.startswith(m.folder + "/")), None)
        write_page(docpath, data, mat)
    build_home()

    with open(os.path.join(DOCS, "404.html"), "w", encoding="utf-8") as f:
        f.write(BASE_T.substitute(title="Page not found", root="./", crumbs="", sidebar="", kicker="",
                                  h1block="<h1>Page not found</h1>", meta_html="",
                                  body='<p>That page is not on the site. The material map:</p>' +
                                       "".join(f'<p><a href="{m.folder}/index.html">{esc(m.name)}</a></p>' for m in MATS),
                                  toc="", pager=""))

    adir = os.path.join(DOCS, "assets")
    os.makedirs(adir, exist_ok=True)
    a_src = os.path.join(HERE, "assets")
    for f in os.listdir(a_src):
        if f != "search-index.json":
            shutil.copy2(os.path.join(a_src, f), os.path.join(adir, f))
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    with open(os.path.join(adir, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(SEARCH, f, ensure_ascii=False)

    print(f"built {len(PAGES) + 2} pages + assets into docs/ (search index: {len(SEARCH)} entries)")


if __name__ == "__main__":
    main()
