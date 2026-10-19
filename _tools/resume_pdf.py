#!/usr/bin/env python3
"""Render resume.md -> public/Yan_Qi_Resume.pdf.

Pure standard library (no pip installs): parses the TrueType font directly and
embeds it, lays out the resume markdown subset used in resume.md (headings,
bold/italic, links, two bullet levels). Jekyll ignores this folder (leading _).

Usage (from repo root):  python3 _tools/resume_pdf.py
Fonts: Arial (macOS) or DejaVu Sans (Linux); override with FONT_REGULAR / FONT_BOLD env vars.
"""
import os
import re
import struct
import sys
import zlib

SRC = "resume.md"
OUT = "public/Yan_Qi_Resume.pdf"
def _first(env, *cands):
    for c in ((os.environ.get(env),) if os.environ.get(env) else ()) + cands:
        if os.path.exists(c):
            return c
    raise SystemExit(f"no font found for {env}; set it to a .ttf path")


# macOS Arial first (always present on a Mac), DejaVu Sans as the Linux fallback.
FONT_REGULAR = _first("FONT_REGULAR", "/System/Library/Fonts/Supplemental/Arial.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = _first("FONT_BOLD", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

PAGE_W, PAGE_H = 612, 792            # US Letter
ML, MR, MT, MB = 50, 50, 44, 48       # margins
TEXT_W = PAGE_W - ML - MR
INK = "0.13 0.13 0.13"
ACCENT = "0.11 0.29 0.53"
MUTED = "0.40 0.40 0.40"

WIN_EXTRA = {0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97, 0x2019: 0x92, 0x201C: 0x93, 0x201D: 0x94}


def win_code(ch):
    o = ord(ch)
    if 32 <= o <= 126 or 0xA0 <= o <= 0xFF:
        return o
    if o in WIN_EXTRA:
        return WIN_EXTRA[o]
    raise ValueError(f"character {ch!r} (U+{o:04X}) not representable in WinAnsi")


def win_unicode(code):
    for u, c in WIN_EXTRA.items():
        if c == code:
            return u
    return code


class TTF:
    def __init__(self, path):
        self.path = path
        self.data = d = open(path, "rb").read()
        n = struct.unpack(">H", d[4:6])[0]
        self.tables = {}
        for i in range(n):
            tag, _cs, off, ln = struct.unpack(">4sIII", d[12 + 16 * i:28 + 16 * i])
            self.tables[tag.decode("latin1")] = (off, ln)
        off = self.tables["head"][0]
        self.upem = struct.unpack(">H", d[off + 18:off + 20])[0]
        self.bbox = struct.unpack(">hhhh", d[off + 36:off + 44])
        off = self.tables["hhea"][0]
        self.asc, self.desc = struct.unpack(">hh", d[off + 4:off + 8])
        nhm = struct.unpack(">H", d[off + 34:off + 36])[0]
        off = self.tables["hmtx"][0]
        self.adv = [struct.unpack(">H", d[off + 4 * i:off + 4 * i + 2])[0] for i in range(nhm)]
        self.cmap = self._cmap()
        name = os.path.splitext(os.path.basename(path))[0]
        self.name = re.sub(r"[^A-Za-z0-9-]", "", name)
        self.widths = [self._w1000(win_unicode(c)) for c in range(32, 256)]

    def _cmap(self):
        d = self.data
        base = self.tables["cmap"][0]
        n = struct.unpack(">H", d[base + 2:base + 4])[0]
        sub = None
        for i in range(n):
            pid, eid, off = struct.unpack(">HHI", d[base + 4 + 8 * i:base + 12 + 8 * i])
            if pid == 3 and eid == 1:
                sub = base + off
        if sub is None or struct.unpack(">H", d[sub:sub + 2])[0] != 4:
            raise SystemExit(f"{self.path}: no (3,1) format-4 cmap")
        segx2 = struct.unpack(">H", d[sub + 6:sub + 8])[0]
        seg = segx2 // 2
        ends = struct.unpack(f">{seg}H", d[sub + 14:sub + 14 + segx2])
        p = sub + 16 + segx2
        starts = struct.unpack(f">{seg}H", d[p:p + segx2]); p += segx2
        deltas = struct.unpack(f">{seg}h", d[p:p + segx2]); p += segx2
        roff_pos = p
        roffs = struct.unpack(f">{seg}H", d[p:p + segx2])
        m = {}
        for i in range(seg):
            for c in range(starts[i], min(ends[i], 0x2FFF) + 1):
                if roffs[i] == 0:
                    g = (c + deltas[i]) & 0xFFFF
                else:
                    a = roff_pos + 2 * i + roffs[i] + 2 * (c - starts[i])
                    g = struct.unpack(">H", d[a:a + 2])[0]
                    if g:
                        g = (g + deltas[i]) & 0xFFFF
                m[c] = g
        return m

    def _w1000(self, u):
        g = self.cmap.get(u, 0)
        return round(self.adv[min(g, len(self.adv) - 1)] * 1000 / self.upem)

    def width(self, text, size):
        return sum(self.widths[win_code(ch) - 32] for ch in text) * size / 1000


FONTS = {False: TTF(FONT_REGULAR), True: TTF(FONT_BOLD)}
FONT_RES = {False: "F1", True: "F2"}


def pdf_str(text):
    b = bytes(win_code(ch) for ch in text)
    return b"(" + b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"


# ---------------------------------------------------------------- markdown --
INLINE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|\*(.+?)\*")


def runs(text, bold=False, italic=False):
    """-> list of (text, bold, italic, url)."""
    out, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], bold, italic, None))
        if m.group(1) is not None:
            out.append((m.group(1), bold, italic, m.group(2)))
        elif m.group(3) is not None:
            out += runs(m.group(3), True, italic)
        else:
            out += runs(m.group(4), bold, True)
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], bold, italic, None))
    return out


def blocks(md):
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)    # front matter
    out, first_h2 = [], True
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip() == "---":
            continue
        if "Yan_Qi_Resume.pdf" in line:      # the web page's own download link
            continue
        if line.startswith("## "):
            out.append(("name" if first_h2 else "h2", line[3:]))
            first_h2 = False
        elif line.startswith("#### "):
            out.append(("h4", line[5:]))
        elif line.startswith("### "):
            out.append(("h3", line[4:]))
        elif re.match(r"^  +- ", line):
            out.append(("li2", line.strip()[2:]))
        elif line.startswith("- "):
            out.append(("li1", line[2:]))
        else:
            out.append(("p", line))
    return out


# ------------------------------------------------------------------ layout --
STYLE = {  # kind: (size, leading, space_before, indent, bullet, base_bold, color, center)
    "name": (21, 25, 0, 0, None, True, INK, True),
    "tag":  (9.4, 12.5, 2, 0, None, False, ACCENT, True),
    "contact": (9, 12, 1, 0, None, False, MUTED, True),
    "h2":   (11.5, 14, 8, 0, None, True, ACCENT, False),
    "h3":   (10.5, 13, 5, 0, None, True, INK, False),
    "h4":   (9.8, 12.5, 3, 0, None, True, INK, False),
    "p":    (8.7, 11.0, 1.5, 0, None, False, INK, False),
    "li1":  (8.7, 11.0, 1.2, 11, "\u2022", False, INK, False),
    "li2":  (8.7, 11.0, 0.8, 23, "\u2013", False, INK, False),
}


class Doc:
    def __init__(self):
        self.pages = []          # list of (content_ops list, annots list)
        self.new_page()

    def new_page(self):
        self.ops, self.annots = [], []
        self.pages.append((self.ops, self.annots))
        self.y = PAGE_H - MT

    def ensure(self, h):
        if self.y - h < MB:
            self.new_page()
            return True
        return False

    def wrap(self, rs, size, width):
        pieces = []
        for text, b, i, url in rs:
            for tok in re.findall(r"\S+|\s+", text):
                pieces.append((" " if tok.isspace() else tok, b, i, url))
        lines, cur, cur_w = [], [], 0.0
        for p in pieces:
            w = FONTS[p[1]].width(p[0], size)
            if p[0] == " ":
                if cur:
                    cur.append(p); cur_w += w
                continue
            if cur and cur_w + w > width:
                while cur and cur[-1][0] == " ":
                    cur_w -= FONTS[cur[-1][1]].width(" ", size); cur.pop()
                lines.append(cur); cur, cur_w = [], 0.0
            cur.append(p); cur_w += w
        while cur and cur[-1][0] == " ":
            cur.pop()
        if cur:
            lines.append(cur)
        return lines

    def draw_line(self, line, x, y, size, color, center):
        width = sum(FONTS[b].width(t, size) for t, b, _i, _u in line)
        if center:
            x = ML + (TEXT_W - width) / 2
        self.ops.append(f"BT {color} rg")
        for t, b, i, url in line:
            w = FONTS[b].width(t, size)
            shear = "0.2" if i else "0"
            col = ACCENT if url else color
            self.ops.append(f"{col} rg /{FONT_RES[b]} {size} Tf 1 0 {shear} 1 {x:.2f} {y:.2f} Tm")
            self.ops.append(pdf_str(t).decode("latin1") + " Tj")
            if url and t != " ":
                self.annots.append((x, y - 2, x + w, y + size * 0.8, url))
            x += w
        self.ops.append("ET")

    def block(self, kind, text, keep_with_next=0):
        size, lead, before, indent, bullet, bold, color, center = STYLE[kind]
        lines = self.wrap(runs(text, bold), size, TEXT_W - indent)
        if self.y != PAGE_H - MT:
            self.y -= before
        self.ensure(lead * len(lines[:2]) + keep_with_next)
        for n, line in enumerate(lines):
            if n:
                self.ensure(lead)
            self.y -= lead
            base = self.y + (lead - size) * 0.35
            if bullet and n == 0:
                self.draw_line([(bullet, False, False, None)], ML + indent - 9, base, size, MUTED, False)
            self.draw_line(line, ML + indent, base, size, color, center)
        if kind == "h2":
            y = self.y - 2.5
            self.ops.append(f"{ACCENT} RG 0.6 w {ML} {y:.2f} m {PAGE_W - MR} {y:.2f} l S")
            self.y -= 3

    def footer(self):
        total = len(self.pages)
        for n, (ops, _a) in enumerate(self.pages, 1):
            label = f"Yan Qi \u00b7 Resume \u00b7 {n} / {total}"
            w = FONTS[False].width(label, 7.5)
            ops.append(f"BT {MUTED} rg /F1 7.5 Tf 1 0 0 1 {(PAGE_W - w) / 2:.2f} 30 Tm {pdf_str(label).decode('latin1')} Tj ET")


def layout(md):
    doc = Doc()
    bl = blocks(md)
    for idx, (kind, text) in enumerate(bl):
        if idx == 1 and kind == "p":
            kind = "tag"
        elif idx == 2 and kind == "p":
            kind = "contact"
        keep = {"h2": 40, "h3": 30, "h4": 25}.get(kind, 0)
        if kind == "li1" and text.rstrip().endswith((":**", ":")):
            keep = 24          # bullet that introduces sub-bullets: keep with them
        doc.block(kind, text, keep)
    doc.footer()
    return doc


# --------------------------------------------------------------- PDF write --
def write_pdf(doc, path):
    objs = []

    def add(body):
        objs.append(body)
        return len(objs)

    def stream(data, extra=""):
        comp = zlib.compress(data, 9)
        return f"<< /Length {len(comp)} /Filter /FlateDecode {extra}>>\nstream\n".encode() + comp + b"\nendstream"

    catalog = add(None)
    pages_id = add(None)
    font_ids = {}
    for bold, f in FONTS.items():
        ff = add(stream(f.data, f"/Length1 {len(f.data)} "))
        sc = 1000 / f.upem
        bb = " ".join(str(round(v * sc)) for v in f.bbox)
        desc = add(f"<< /Type /FontDescriptor /FontName /{f.name} /Flags 32 /FontBBox [{bb}] "
                   f"/ItalicAngle 0 /Ascent {round(f.asc * sc)} /Descent {round(f.desc * sc)} "
                   f"/CapHeight {round(f.asc * sc * 0.73)} /StemV {120 if bold else 80} /FontFile2 {ff} 0 R >>".encode())
        font_ids[bold] = add(f"<< /Type /Font /Subtype /TrueType /BaseFont /{f.name} /FirstChar 32 /LastChar 255 "
                             f"/Widths [{' '.join(map(str, f.widths))}] /Encoding /WinAnsiEncoding "
                             f"/FontDescriptor {desc} 0 R >>".encode())
    res = f"<< /Font << /F1 {font_ids[False]} 0 R /F2 {font_ids[True]} 0 R >> >>"
    kids = []
    for ops, annots in doc.pages:
        content = add(stream("\n".join(ops).encode("latin1")))
        aids = []
        for x1, y1, x2, y2, url in annots:
            u = url.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            aids.append(add(f"<< /Type /Annot /Subtype /Link /Rect [{x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f}] "
                            f"/Border [0 0 0] /A << /S /URI /URI ({u}) >> >>".encode()))
        annot = f" /Annots [{' '.join(f'{a} 0 R' for a in aids)}]" if aids else ""
        kids.append(add(f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
                        f"/Resources {res} /Contents {content} 0 R{annot} >>".encode()))
    objs[pages_id - 1] = f"<< /Type /Pages /Kids [{' '.join(f'{k} 0 R' for k in kids)}] /Count {len(kids)} >>".encode()
    objs[catalog - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode()
    info = add(b"<< /Title (Yan Qi - Resume) /Author (Yan Qi) /Subject (Senior Engineering Leader - Data Platform & Infrastructure) >>")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for o in offsets:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root {catalog} 0 R /Info {info} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    with open(path, "wb") as fh:
        fh.write(out)
    return len(doc.pages), len(out)


if __name__ == "__main__":
    md = open(SRC, encoding="utf-8").read()
    doc = layout(md)
    pages, size = write_pdf(doc, OUT)
    used = (PAGE_H - MT - doc.y) / (PAGE_H - MT - MB)
    print(f"wrote {OUT}: {pages} page(s), {size} bytes, last page {used:.0%} full")
