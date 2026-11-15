#!/usr/bin/env python3
"""
Editable concept diagram for proxmox-steam-gpu-mosu-sc2-emudeck.

Style: manzoku.blog (paper + ink + orange, hard borders, serif/mono).
Output: concept/concept-manzoku.png (@2x, committed) + concept/concept-manzoku.svg
(local by-product, git-ignored).

Edit the CONFIG block below, then rebuild from the repo root:

    python3 scripts/concept-diagram/make_concept.py

First run needs the fonts:

    bash scripts/concept-diagram/fetch-fonts.sh

Requires: python3-pil, python3-cairosvg.
"""

from pathlib import Path
import os
import sys

from PIL import ImageFont
import cairosvg

# ============================== CONFIG ==============================

COLORS = {
    "paper":       "#f2ede1",
    "card":        "#fbf8ef",
    "ink":         "#15140f",
    "soft":        "#514b3e",
    "muted":       "#7b7464",
    "accent":      "#df3f1f",   # manzoku orange
    "green":       "#1f5f4a",
    "green_light": "#7cc7a4",
    "line_soft":   "#c8bfab",
}

CANVAS = {"width": 1600, "height": 1264, "scale": 2}

LAYOUT = {
    "build_y": 324, "build_h": 230,
    "runtime_y": 584, "runtime_h": 430,
    "strip_y": 1044, "strip_h": 112,
    "footer_line_y": 1184, "footer_text_y": 1205, "footer_credit_y": 1231,
}

OUTPUT = {
    "svg": "concept/concept-manzoku.svg",
    "png": "concept/concept-manzoku.png",
}

TEXT = {
    # header
    "brand": "MANZOKU",
    "brand_sub": "満足 / HOMELAB NOTES",
    "site": "MANZOKU.BLOG",
    "site_sub": "PROXMOX · STEAMOS · GPU · MOONLIGHT",

    # hero
    "kicker": "CONCEPT DIAGRAM — ZERO-TOUCH TO GAME",
    "headline_a": "One box.",
    "headline_b": " Every screen.",
    "sub_a": "A Proxmox VE host that behaves like a Steam Deck: SteamOS VM, RTX 3070",
    "sub_b": "passed through, Steam Controller 2 on USB — Sunshine streams it to any screen.",

    # build panel
    "build_title": "THE BUILD",
    "build_note": "ONE-TIME / NO PROMPTS / NO CLICKS",
    "build_chip": "PACKER",
    "build_inputs": ["bazzite-stable-amd64.iso", "steamos-ks.cfg"],
    "build_cmd": "packer build",
    "build_script": "build-linux-iso.sh",
    "build_cmdline": "inst.ks=cdrom:/steamos-ks.cfg",
    "build_output": "autoinstall.iso",
    "build_output_sub": "kickstart baked in",
    "build_output_path": "hdd-iso:iso/",
    "build_tf_key": "autoinstall_enabled",
    "build_tf_val": "= true",
    "build_tf_note": "cdrom",
    "build_tf_caption": "VM BOOTS FROM THE BUILT ISO",
    "build_caption": "UPLOAD THE BUILT ISO ONCE → SET autoinstall_enabled → TERRAFORM DOES THE REST",

    # runtime panel
    "runtime_title": "THE PIPELINE",
    "runtime_note": "ONE PHYSICAL PC / AS MANY SCREENS AS YOU WANT",
    "runtime_chip": "TCP 47989",
    "clients": [("TV", "Apple TV 4K", "4K HDR"), ("NB", "Notebook", "LAN"), ("PH", "Phone", "WAN")],
    "host_title": "Sunshine",
    "host_port": ":47989",
    "gpu": "RTX 3070",   # generic label; set to whatever card you want shown
    "gpu_chip": "VFIO",
    "host_caption": "IOMMU · HOSTPCI0 · XVGA · ROMBAR OFF",
    "vm_title": "Bazzite",
    "vm_tag": "GUEST",
    "vm_auto_chip": "AUTO",
    "vm_chips": [
        ("EmuDeck", 100, True), ("Steam", 74, False),
        ("Dolphin", 84, False), ("PCSX2", 80, False), ("RetroArch", 100, False),
    ],
    "vm_caption": "8 vCPU · 16 GB RAM · 500 GB",
    "game_kicker": "LIVE",
    "game_title": "Game",
    "game_caption": "VIA SUNSHINE",

    # quote + controller
    "quote_a": "“The Deck is the host, the screen is",
    "quote_b": "whatever client I pick.”",
    "quote_attr": "ARWID — README.MD",
    "controller_title": "Steam Controller 2",
    "controller_sub": "USB PASSTHROUGH · SC2 → XBOX 360 · SDL2 + DOLPHIN",
    "controller_chip": "USB",

    # bottom strip
    "strip": [
        ("THE HOST", "Proxmox VE 8", "X570D4U · RYZEN 9 5900XT"),
        ("THE GUEST", "SteamOS / Bazzite", "8 vCPU · 16 GB · 500 GB · VIRTIO"),
        ("THE STREAM", "Sunshine + Moonlight", "TCP 47989 · APPLE TV 4K · 2 PADS"),
    ],

    # footer
    "footer_left": "MANZOKU.BLOG",
    "footer_center": "満足 · ENOUGH IS THE NEW MORE",
    "footer_right": "PROXMOX-STEAM-GPU-MOSU-SC2-EMUDECK",
    "footer_credit_left": "CREATED BY ARWID R.",
    "footer_credit_right": "© 2026 ARWID R. · ALL RIGHTS RESERVED",
}

# ============================ /CONFIG ==============================

ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = Path(os.environ.get("MANZOKU_FONTS", Path.home() / ".local/share/fonts/manzoku"))
FONT_FILES = {
    ("Fraunces", 400): FONT_DIR / "fraunces-400.ttf",
    ("Fraunces", 600): FONT_DIR / "fraunces-600.ttf",
    ("Fraunces", 700): FONT_DIR / "fraunces-700.ttf",
    ("Fraunces", 900): FONT_DIR / "fraunces-900.ttf",
    ("JetBrains Mono", 400): FONT_DIR / "jbm-400.ttf",
    ("JetBrains Mono", 700): FONT_DIR / "jbm-700.ttf",
    ("Zen Kaku Gothic New", 400): FONT_DIR / "ZenKakuGothicNew-Regular.ttf",
    ("Zen Kaku Gothic New", 500): FONT_DIR / "ZenKakuGothicNew-Medium.ttf",
    ("Zen Kaku Gothic New", 700): FONT_DIR / "ZenKakuGothicNew-Bold.ttf",
}

missing = [p.name for p in FONT_FILES.values() if not p.exists()]
if missing:
    sys.exit(
        "Missing fonts: " + ", ".join(sorted(set(missing))) + "\n"
        "Run: bash scripts/concept-diagram/fetch-fonts.sh\n"
        f"(or set MANZOKU_FONTS to the directory that holds them; current: {FONT_DIR})"
    )

PAPER, CARD, INK, SOFT = COLORS["paper"], COLORS["card"], COLORS["ink"], COLORS["soft"]
MUTED, ACCENT, GREEN, GREEN_L, LS = (
    COLORS["muted"], COLORS["accent"], COLORS["green"], COLORS["green_light"], COLORS["line_soft"])
W, H = CANVAS["width"], CANVAS["height"]

_face_cache = {}

def measure(s, family="Zen Kaku Gothic New", size=14, weight=400, ls=0.0):
    key = (family, size, weight)
    if key not in _face_cache:
        _face_cache[key] = ImageFont.truetype(str(FONT_FILES[(family, weight)]), size)
    return _face_cache[key].getlength(s) + max(0, len(s) - 1) * ls

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, family="Zen Kaku Gothic New", size=14, weight=400,
         fill=INK, ls=0.0, anchor="start", opacity=1.0, cap=None):
    width = measure(s, family, size, weight, ls)
    if cap is not None and width > cap + 0.5:
        print(f"WARNING text wider than its box ({width:.0f} > {cap:.0f}): {s[:60]!r}")
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}" opacity="{opacity}">{esc(s)}</text>')

cur, txt = [], []   # shape layer / text layer

def shadow_rect(x, y, wd, ht, dx=6, dy=6):
    return f'<rect x="{x+dx}" y="{y+dy}" width="{wd}" height="{ht}" fill="{INK}"/>'

def card(x, y, wd, ht, fill=CARD, dx=6, dy=6):
    return (shadow_rect(x, y, wd, ht, dx, dy) +
            f'<rect x="{x}" y="{y}" width="{wd}" height="{ht}" fill="{fill}" '
            f'stroke="{INK}" stroke-width="1.5"/>')

def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None):
    s = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" '
         f'stroke-width="1.5" marker-end="url(#ah)"/>')
    if label:
        s += text(lx if lx is not None else (x1 + x2) / 2,
                  ly if ly is not None else y1 - 9,
                  label, "JetBrains Mono", 8, 400, MUTED, ls=1.6, anchor="middle")
    return s

def header():
    cur.append(f'<line x1="0" y1="88.5" x2="{W}" y2="88.5" stroke="{INK}" stroke-width="1.5"/>')
    cur.append(shadow_rect(64, 24, 44, 44, 3, 3))
    cur.append(f'<rect x="64" y="24" width="44" height="44" fill="{ACCENT}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(86, 56, "満", "Zen Kaku Gothic New", 27, 700, "#ffffff", anchor="middle"))
    txt.append(text(122, 47, TEXT["brand"], "Fraunces", 22, 700, INK, ls=2.4))
    txt.append(text(124, 64, TEXT["brand_sub"], "JetBrains Mono", 8, 400, MUTED, ls=2.2))
    txt.append(text(1536, 47, TEXT["site"], "JetBrains Mono", 10, 400, ACCENT, ls=2.4, anchor="end"))
    txt.append(text(1536, 65, TEXT["site_sub"], "JetBrains Mono", 8, 400, MUTED, ls=2.0, anchor="end"))

def hero():
    txt.append(text(64, 142, TEXT["kicker"], "JetBrains Mono", 11, 400, ACCENT, ls=3.0))
    size = 84
    wa = measure(TEXT["headline_a"], "Fraunces", size, 700)
    wb = measure(TEXT["headline_b"], "Fraunces", size, 700)
    cur.append(f'<rect x="{64 + wa + 12}" y="232" width="{wb - 8}" height="10" fill="{ACCENT}" opacity="0.22"/>')
    txt.append(text(64, 228, TEXT["headline_a"], "Fraunces", size, 700, INK))
    txt.append(text(64 + wa + 8, 228, TEXT["headline_b"], "Fraunces", size, 700, ACCENT))
    txt.append(text(64, 276, TEXT["sub_a"], "Zen Kaku Gothic New", 16.5, 400, SOFT, cap=1050))
    txt.append(text(64, 300, TEXT["sub_b"], "Zen Kaku Gothic New", 16.5, 400, SOFT, cap=1050))
    # manzoku stamp
    cur.append('<g transform="rotate(-7 1392 206)">')
    cur.append(f'<rect x="1341" y="155" width="104" height="104" fill="{INK}"/>')
    cur.append(f'<rect x="1336" y="150" width="104" height="104" fill="{ACCENT}" stroke="{INK}" stroke-width="1.5"/>')
    cur.append(f'<rect x="1345" y="159" width="86" height="86" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.85"/>')
    cur.append('<text x="1388" y="201" font-family="Zen Kaku Gothic New" font-size="30" font-weight="700" '
               'fill="#ffffff" text-anchor="middle" letter-spacing="4">満足</text>')
    cur.append('<text x="1388" y="224" font-family="JetBrains Mono" font-size="7" font-weight="700" '
               'fill="#ffffff" text-anchor="middle" letter-spacing="2.2">MANZOKU</text>')
    cur.append('</g>')

def build_panel(y):
    cur.append(card(64, y, 1472, LAYOUT["build_h"], CARD, 8, 8))
    txt.append(text(96, y + 35, TEXT["build_title"], "JetBrains Mono", 10, 400, SOFT, ls=3.2))
    txt.append(text(1045, y + 35, TEXT["build_note"], "JetBrains Mono", 8, 400, MUTED, ls=1.8, anchor="end"))
    cur.append(f'<rect x="1380" y="{y+17}" width="124" height="25" fill="{ACCENT}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(1442, y + 34, TEXT["build_chip"], "JetBrains Mono", 9.5, 700, "#ffffff", ls=1.6, anchor="middle"))
    cur.append(f'<line x1="96" y1="{y+52}" x2="1504" y2="{y+52}" stroke="{LS}" stroke-width="1.5"/>')

    cw, gap, ch = 319, 44, 110
    xs = [96 + i * (cw + gap) for i in range(4)]
    for x in xs:
        cur.append(f'<rect x="{x}" y="{y+74}" width="{cw}" height="{ch}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')

    # 01 inputs
    x = xs[0]
    txt.append(text(x + 20, y + 100, "01 / INPUTS", "JetBrains Mono", 9, 400, MUTED, ls=2.2))
    for i, name in enumerate(TEXT["build_inputs"]):
        yy = y + 116 + i * 32
        cur.append(f'<rect x="{x+20}" y="{yy}" width="{cw-40}" height="26" fill="{CARD}" stroke="{INK}" stroke-width="1.2"/>')
        txt.append(text(x + 32, yy + 17, name, "JetBrains Mono", 8, 400, INK, ls=0.6, cap=cw - 56))
        txt.append(text(x + cw - 30, yy + 17, ("ISO", "KS")[i], "JetBrains Mono", 7, 700,
                        (ACCENT, GREEN)[i], ls=1.0, anchor="end"))

    # 02 build
    x = xs[1]
    txt.append(text(x + 20, y + 100, "02 / BUILD", "JetBrains Mono", 9, 400, MUTED, ls=2.2))
    txt.append(text(x + 20, y + 140, TEXT["build_cmd"], "Fraunces", 20, 700, INK))
    txt.append(text(x + 20, y + 162, TEXT["build_script"], "JetBrains Mono", 8, 400, INK, ls=0.4, cap=cw - 40))
    txt.append(text(x + 20, y + 178, TEXT["build_cmdline"], "JetBrains Mono", 7.2, 400, SOFT, ls=0.3, cap=cw - 40))

    # 03 output
    x = xs[2]
    txt.append(text(x + 20, y + 100, "03 / OUTPUT", "JetBrains Mono", 9, 400, MUTED, ls=2.2))
    txt.append(text(x + 20, y + 142, TEXT["build_output"], "Fraunces", 20, 700, INK, cap=cw - 40))
    txt.append(text(x + 20, y + 164, TEXT["build_output_sub"], "JetBrains Mono", 8, 400, SOFT, ls=0.6, cap=cw - 40))
    txt.append(text(x + 20, y + 180, TEXT["build_output_path"], "JetBrains Mono", 7.5, 400, MUTED, ls=0.8))

    # 04 terraform
    x = xs[3]
    txt.append(text(x + 20, y + 100, "04 / TERRAFORM", "JetBrains Mono", 9, 400, MUTED, ls=2.2))
    cur.append(f'<rect x="{x+20}" y="{y+114}" width="{cw-40}" height="56" fill="{INK}"/>')
    txt.append(text(x + 32, y + 134, TEXT["build_tf_key"], "JetBrains Mono", 8.5, 400, "#ffffff", ls=0.4))
    txt.append(text(x + 32, y + 154, TEXT["build_tf_val"], "JetBrains Mono", 9.5, 700, GREEN_L, ls=1.0))
    txt.append(text(x + cw - 30, y + 154, TEXT["build_tf_note"], "JetBrains Mono", 7.5, 400, "#8d8676", anchor="end"))
    txt.append(text(x + 20, y + 181, TEXT["build_tf_caption"], "JetBrains Mono", 7, 400, MUTED, ls=1.0, cap=cw - 40))

    for i in range(3):
        cur.append(arrow(xs[i] + cw + 4, y + 129, xs[i + 1] - 5, y + 129))
    txt.append(text(96, y + 212, TEXT["build_caption"], "JetBrains Mono", 8, 400, SOFT, ls=1.6, cap=1408))

def runtime_panel(y):
    cur.append(card(64, y, 1472, LAYOUT["runtime_h"], CARD, 8, 8))
    txt.append(text(96, y + 35, TEXT["runtime_title"], "JetBrains Mono", 10, 400, SOFT, ls=3.2))
    txt.append(text(1045, y + 35, TEXT["runtime_note"], "JetBrains Mono", 8, 400, MUTED, ls=1.8, anchor="end"))
    cur.append(f'<rect x="1380" y="{y+17}" width="124" height="25" fill="{ACCENT}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(1442, y + 34, TEXT["runtime_chip"], "JetBrains Mono", 9.5, 700, "#ffffff", ls=1.2, anchor="middle"))
    cur.append(f'<line x1="96" y1="{y+52}" x2="1504" y2="{y+52}" stroke="{LS}" stroke-width="1.5"/>')

    cy, ch = y + 74, 184
    mid = cy + 92

    # 05 clients
    cur.append(f'<rect x="96" y="{cy}" width="330" height="{ch}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(116, cy + 26, "05 / CLIENTS", "JetBrains Mono", 9.5, 400, MUTED, ls=2.4))
    yy = cy + 40
    for tag, name, meta in TEXT["clients"]:
        cur.append(f'<rect x="116" y="{yy}" width="290" height="36" fill="{CARD}" stroke="{INK}" stroke-width="1.2"/>')
        cur.append(f'<rect x="121" y="{yy+6}" width="24" height="24" fill="{ACCENT}"/>')
        txt.append(text(133, yy + 23, tag, "JetBrains Mono", 8, 700, "#ffffff", ls=0.5, anchor="middle"))
        txt.append(text(155, yy + 23, name, "Zen Kaku Gothic New", 13.5, 500, INK))
        txt.append(text(398, yy + 23, meta, "JetBrains Mono", 8, 400, MUTED, anchor="end"))
        yy += 44
    cur.append(arrow(426, mid, 492, mid, "STREAM", 459, mid - 10))

    # 06 host
    cur.append(f'<rect x="492" y="{cy}" width="396" height="{ch}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(512, cy + 26, "06 / PROXMOX HOST", "JetBrains Mono", 9.5, 400, MUTED, ls=2.4))
    cur.append(f'<rect x="512" y="{cy+40}" width="356" height="44" fill="{ACCENT}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(528, cy + 68, TEXT["host_title"], "Zen Kaku Gothic New", 16, 700, "#ffffff"))
    txt.append(text(852, cy + 68, TEXT["host_port"], "JetBrains Mono", 9, 400, "#ffffff", ls=0.5, anchor="end"))
    cur.append(f'<rect x="512" y="{cy+94}" width="356" height="44" fill="{CARD}" stroke="{INK}" stroke-width="1.5"/>')
    cur.append(f'<rect x="512" y="{cy+94}" width="5" height="44" fill="{GREEN}"/>')
    txt.append(text(528, cy + 122, TEXT["gpu"], "Fraunces", 19, 700, INK))
    cur.append(f'<rect x="790" y="{cy+102}" width="60" height="28" fill="{GREEN}" stroke="{INK}" stroke-width="1.2"/>')
    txt.append(text(820, cy + 120, TEXT["gpu_chip"], "JetBrains Mono", 8.5, 700, "#ffffff", ls=1.2, anchor="middle"))
    txt.append(text(512, cy + 168, TEXT["host_caption"], "JetBrains Mono", 8, 400, MUTED, ls=1.4, cap=356))
    cur.append(arrow(888, mid, 952, mid, "PCIe", 920, mid - 10))

    # 07 VM
    cur.append(f'<rect x="952" y="{cy}" width="316" height="{ch}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(972, cy + 26, "07 / STEAMOS VM", "JetBrains Mono", 9.5, 400, MUTED, ls=2.4))
    cur.append(f'<rect x="1188" y="{cy+13}" width="62" height="19" fill="{ACCENT}" stroke="{INK}" stroke-width="1.2"/>')
    txt.append(text(1219, cy + 26, TEXT["vm_auto_chip"], "JetBrains Mono", 7.5, 700, "#ffffff", ls=1.4, anchor="middle"))
    txt.append(text(972, cy + 66, TEXT["vm_title"], "Fraunces", 25, 700, INK))
    txt.append(text(1250, cy + 66, TEXT["vm_tag"], "JetBrains Mono", 7.5, 400, MUTED, ls=2.0, anchor="end"))

    chip_y = cy + 80
    row1 = TEXT["vm_chips"][:2]
    row2 = TEXT["vm_chips"][2:]
    x = 972
    for label, wd, filled in row1:
        cur.append(f'<rect x="{x}" y="{chip_y}" width="{wd}" height="28" fill="{GREEN if filled else CARD}" '
                   f'stroke="{INK}" stroke-width="1.2"/>')
        txt.append(text(x + wd / 2, chip_y + 18.5, label, "JetBrains Mono", 8.5, 400,
                        "#ffffff" if filled else INK, anchor="middle"))
        x += wd + 6
    x = 972
    for label, wd, filled in row2:
        cur.append(f'<rect x="{x}" y="{chip_y+34}" width="{wd}" height="28" fill="{GREEN if filled else CARD}" '
                   f'stroke="{INK}" stroke-width="1.2"/>')
        txt.append(text(x + wd / 2, chip_y + 52.5, label, "JetBrains Mono", 8.5, 400,
                        "#ffffff" if filled else INK, anchor="middle"))
        x += wd + 6
    txt.append(text(972, cy + 170, TEXT["vm_caption"], "JetBrains Mono", 8, 400, MUTED, ls=1.2, cap=296))
    cur.append(arrow(1268, mid, 1330, mid, "PLAY", 1299, mid - 10))

    # 08 game
    cur.append(f'<rect x="1336" y="{cy}" width="168" height="{ch}" fill="{GREEN}" stroke="{INK}" stroke-width="1.5"/>')
    cur.append(f'<rect x="1342" y="{cy+6}" width="156" height="{ch-12}" fill="none" stroke="{GREEN_L}" stroke-width="1" opacity="0.8"/>')
    txt.append(text(1420, cy + 38, TEXT["game_kicker"], "JetBrains Mono", 8, 400, GREEN_L, ls=2.4, anchor="middle"))
    txt.append(text(1420, cy + 92, TEXT["game_title"], "Fraunces", 34, 700, "#ffffff", anchor="middle"))
    cur.append(f'<line x1="1374" y1="{cy+112}" x2="1466" y2="{cy+112}" stroke="#ffffff" stroke-width="1" opacity="0.45"/>')
    txt.append(text(1420, cy + 142, TEXT["game_caption"], "JetBrains Mono", 7.5, 400, "#ffffff", ls=1.5,
                    anchor="middle", opacity=0.9))

    # quote
    qy, qx, qw, qh = y + 298, 96, 716, 102
    cur.append(f'<rect x="{qx}" y="{qy}" width="{qw}" height="{qh}" fill="{CARD}" stroke="{INK}" stroke-width="1.5"/>')
    cur.append(f'<rect x="{qx}" y="{qy}" width="6" height="{qh}" fill="{ACCENT}"/>')
    txt.append(f'<g transform="translate(126,{qy+36}) skewX(-8)">' +
               text(0, 0, TEXT["quote_a"], "Fraunces", 23, 400, INK) +
               text(0, 30, TEXT["quote_b"], "Fraunces", 23, 400, INK) + '</g>')
    txt.append(text(126, qy + 86, TEXT["quote_attr"], "JetBrains Mono", 8, 400, MUTED, ls=2.2))

    # controller
    kx, ky, kw, kh = 952, y + 298, 552, 102
    cur.append(f'<rect x="{kx}" y="{ky}" width="{kw}" height="{kh}" fill="{CARD}" stroke="{INK}" stroke-width="1.5"/>')
    txt.append(text(972, ky + 23, "08 / INPUT", "JetBrains Mono", 8.5, 400, MUTED, ls=2.2))
    txt.append(text(972, ky + 55, TEXT["controller_title"], "Fraunces", 23, 700, INK))
    txt.append(text(972, ky + 78, TEXT["controller_sub"], "JetBrains Mono", 8, 400, SOFT, ls=1.2, cap=512))
    cur.append(f'<rect x="1440" y="{ky+16}" width="44" height="18" fill="{ACCENT}" stroke="{INK}" stroke-width="1.2"/>')
    txt.append(text(1462, ky + 29, TEXT["controller_chip"], "JetBrains Mono", 7.5, 700, "#ffffff", ls=1.0, anchor="middle"))
    cur.append(f'<line x1="1110" y1="{ky-2}" x2="1110" y2="{cy+ch+6}" stroke="{INK}" stroke-width="1.5" marker-end="url(#ah)"/>')
    txt.append(text(1120, ky - 12, "USB 3", "JetBrains Mono", 7.5, 400, MUTED, ls=1.0))

def bottom_strip(y):
    for i, (kick, title, sub) in enumerate(TEXT["strip"]):
        x, wd = 64 + i * 500, 472
        cur.append(card(x, y, wd, LAYOUT["strip_h"], CARD, 6, 6))
        txt.append(text(x + 22, y + 30, kick, "JetBrains Mono", 9, 400, ACCENT, ls=2.6))
        txt.append(text(x + 22, y + 70, title, "Fraunces", 25, 700, INK, cap=wd - 44))
        txt.append(text(x + 22, y + 92, sub, "JetBrains Mono", 8, 400, MUTED, ls=1.4, cap=wd - 44))
        txt.append(text(x + wd - 24, y + 96, f"{i+1:02d}", "Fraunces", 68, 700, INK, anchor="end", opacity=0.09))

def footer(line_y, text_y, credit_y):
    cur.append(f'<line x1="64" y1="{line_y}" x2="1536" y2="{line_y}" stroke="{LS}" stroke-width="1.5"/>')
    cur.append(f'<rect x="64" y="{text_y-11}" width="12" height="12" fill="{ACCENT}" stroke="{INK}" stroke-width="1.2"/>')
    txt.append(text(88, text_y, TEXT["footer_left"], "JetBrains Mono", 9, 700, INK, ls=2.2))
    txt.append(text(800, text_y, TEXT["footer_center"], "JetBrains Mono", 8.5, 400, MUTED, ls=2.0, anchor="middle"))
    txt.append(text(1536, text_y, TEXT["footer_right"], "JetBrains Mono", 8, 400, MUTED, ls=1.2, anchor="end"))
    txt.append(text(88, credit_y, TEXT["footer_credit_left"], "JetBrains Mono", 7.5, 400, MUTED, ls=1.6))
    txt.append(text(1536, credit_y, TEXT["footer_credit_right"], "JetBrains Mono", 7.5, 400, MUTED, ls=1.4, anchor="end"))

def main():
    cur.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    cur.append('''<defs>
  <radialGradient id="glowA" gradientUnits="userSpaceOnUse" cx="150" cy="-90" r="760">
    <stop offset="0" stop-color="#df3f1f" stop-opacity="0.13"/>
    <stop offset="1" stop-color="#df3f1f" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" gradientUnits="userSpaceOnUse" cx="1460" cy="60" r="640">
    <stop offset="0" stop-color="#15140f" stop-opacity="0.07"/>
    <stop offset="1" stop-color="#15140f" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="1.4" cy="1.4" r="0.9" fill="#15140f" opacity="0.10"/>
  </pattern>
  <marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#15140f"/>
  </marker>
</defs>''')
    cur.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    cur.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    cur.append(f'<rect width="{W}" height="{H}" fill="url(#glowA)"/>')
    cur.append(f'<rect width="{W}" height="{H}" fill="url(#glowB)"/>')

    header()
    hero()
    build_panel(LAYOUT["build_y"])
    runtime_panel(LAYOUT["runtime_y"])
    bottom_strip(LAYOUT["strip_y"])
    footer(LAYOUT["footer_line_y"], LAYOUT["footer_text_y"], LAYOUT["footer_credit_y"])

    svg = "\n".join(cur) + "\n" + "\n".join(txt) + "\n</svg>"
    png_path = ROOT / OUTPUT["png"]
    png_path.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.get("svg"):
        svg_path = ROOT / OUTPUT["svg"]
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.write_text(svg, encoding="utf-8")
        print(f"wrote {svg_path.relative_to(ROOT)} (git-ignored)")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(png_path), scale=CANVAS["scale"])
    print(f"wrote {png_path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
