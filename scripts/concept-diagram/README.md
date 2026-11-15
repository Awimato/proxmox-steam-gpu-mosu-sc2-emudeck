# Concept diagram (editable)

Source for `concept/concept-manzoku.png`, the image embedded in the README.

The PNG is generated from a Python script, so the diagram is edit-able: change
text, colors, or panel positions in one config block, rebuild, done. The script
also writes a local `concept/concept-manzoku.svg` (git-ignored) if you want to tweak
it in Inkscape/Figma; only the PNG is committed.

## Quick start

```bash
# once: pip/apt deps + fonts
sudo apt install python3-pil python3-cairosvg
bash scripts/concept-diagram/fetch-fonts.sh

# build (from the repo root, any cwd works)
python3 scripts/concept-diagram/make_concept.py
```

Outputs are written to `concept/concept-manzoku.png` (committed, 1600×1264 @2x =
3200×2528) and `concept/concept-manzoku.svg` (local only, git-ignored).

## Where to edit

Everything sits in the `CONFIG` block at the top of
`scripts/concept-diagram/make_concept.py`:

| Block | What it controls |
| --- | --- |
| `COLORS` | paper, ink, orange accent, green, muted tones |
| `CANVAS` | width, height, PNG scale (`2` = retina) |
| `LAYOUT` | Y positions of the build panel, runtime panel, strip, footer |
| `OUTPUT` | output paths (relative to repo root) |
| `TEXT` | every label: headline, subtitle, card copy, chips, footer |

Text strings live in `TEXT`; layout code below it only places boxes around them.
Search for a label you want to change, edit it in `TEXT`, rebuild.

The script prints `WARNING text wider than its box (...)` when a string no
longer fits. Shorten it, lower the font size in the matching `text(...)` call, or
widen the card.

## Layout map

```
y    0    header (brand + site)
y   96    hero: kicker, headline, subtitle, 満足 stamp
y  324    THE BUILD      (230 tall)  ISO + kickstart -> packer -> ISO -> terraform
y  584    THE PIPELINE   (430 tall)  clients -> host -> VM -> game, controller row
y 1044    bottom strip   (112 tall)  host / guest / stream
y 1184    footer (site, tagline, repo)
y 1231    credit row (created by / copyright)
y 1264    canvas end
```

To add a section: raise `CANVAS.height`, give the new panel its own `LAYOUT`
entry, call it from `main()`, then push the strip/footer down.

## Fonts

`fetch-fonts.sh` downloads OFL fonts into
`${MANZOKU_FONTS:-$HOME/.local/share/fonts/manzoku}` and runs `fc-cache`:

- Fraunces (headlines, 400 / 600 / 700 / 900)
- JetBrains Mono (labels, 400 / 700)
- Zen Kaku Gothic New (満足 and arrows, 400 / 500 / 700)

Cairo resolves fonts by family name through fontconfig, so `MANZOKU_FONTS` must
stay inside a fontconfig-scanned directory (the default does).

## Editing the SVG instead

The script also drops `concept/concept-manzoku.svg` into the working tree (ignored
by git, never committed). Open it in Inkscape/Figma, edit, export PNG. The next
`make_concept.py` run overwrites it, so save a copy if you want to keep manual
edits (`concept-manzoku.v2.svg`).

## Style cheatsheet (manzoku.blog)

- paper `#f2ede1`, card `#fbf8ef`, ink `#15140f`, orange `#df3f1f`, green `#1f5f4a`
- 1.5px ink borders, hard offset shadow (no blur), no rounded corners
- Fraunces for display, JetBrains Mono uppercase + letterspacing for labels
- numbered sections (`01 / INPUTS` …), small dot texture, occasional stamp
