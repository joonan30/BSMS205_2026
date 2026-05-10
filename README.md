# BSMS205 · Genetics — Lecture Slides

Reveal.js slide decks for BSMS205 Genetics (Spring 2026). English. Full course coverage: Chapters 1–30.

## Structure

```
bsms205-slides/
├── index.html              # Course landing · chapter list (Ch 1–30)
├── chapters/
│   ├── chapter1.html       # The Human Genome Project
│   ├── chapter2.html       # T2T Genome Project
│   ├── ...
│   └── chapter30.html      # QTLs
├── assets/
│   ├── css/claude-theme.css
│   └── figures/
│       └── textbook/       # Figures copied from human-genetics textbook
├── docs/
│   ├── 2026-05-11-ch1-19-build-design.md
│   └── 2026-05-11-handoff.md
└── README.md
```

## Design

Claude theme — warm parchment (`#FAF6F1`) with terracotta accent (`#D4724E`).
Helvetica Neue, 28pt+, 16:9, question-driven titles.
See `Slides/CLAUDE.md` in the course folder for the full style guide.

## Viewing locally

No build step. From this directory:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Reveal.js is loaded from jsDelivr CDN — no install required.

### Keyboard

- `→` / `←` — next / previous slide
- `↓` / `↑` — vertical navigation (not used here)
- `F` — fullscreen
- `S` — speaker notes window
- `Esc` — overview
- `B` — blackout
- `?` — all shortcuts

## Deploying to GitHub Pages

```bash
cd bsms205-slides
git init
git add .
git commit -m "Initial slides: Ch 20 Allele Frequency"
gh repo create bsms205-genetics-slides --public --source=. --push
```

Then in the repo:
- **Settings → Pages → Source**: `main` branch, `/ (root)`
- URL: `https://<username>.github.io/bsms205-genetics-slides/`

## PDF export

Append `?print-pdf` to any deck URL and use the browser print dialog:

```
http://localhost:8000/chapters/chapter20.html?print-pdf
```

## Chapter status

All chapters **Ready** (Reveal.js HTML, ~30–50 sections each, 60-min lecture volume, conversational speaker notes, claude-theme components). Ch 1–19 built 2026-05-11 to match the Ch 20–30 pattern; see `docs/2026-05-11-handoff.md` for build notes.

## Textbook

Content adapted from *Human Genetics* textbook (30 chapters, part1–part5).
