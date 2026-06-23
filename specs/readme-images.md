# README Images

## Objective

Generate three visual assets to make the README more attractive and informative: a styled project name banner, a terminal output screenshot of the benchmark report, and matplotlib cost comparison charts. All assets are static images committed to the repo and referenced via markdown.

## Requirements

### Must Have
- **Project name banner**: A styled "LLM Cost Autopilot" header image (PNG) rendered via Python (matplotlib or Pillow) with subtitle "Intelligent Model Routing System". Warm color palette: cream, light brown, light yellow. Placed at the very top of README.
- **Terminal output screenshot**: A PNG image showing the full output of `python run_benchmark.py` (740 prompts, 92.3% cost reduction, 85.4% quality parity, $0.02 vs $0.26, 17.4% escalation rate). Rendered as a faux terminal (dark background, monospace text) via Python.
- **Cost comparison charts (matplotlib)**: Two charts in one PNG image:
  - **Top: Aggregate bar chart** — one bar for routed cost ($0.0204), one for baseline cost ($0.2640), with savings % annotation.
  - **Bottom: Per-tier breakdown** — 3 grouped bar pairs (Tier 1/2/3), routed vs baseline side by side.
  - Warm palette matching the banner.
- All three images saved to a `docs/images/` directory.
- All three images referenced from README.md via standard markdown `![alt](path)`.
- A single Python script `scripts/generate_readme_images.py` that generates all three images in one run.

### Nice to Have
- Faux terminal window chrome (title bar, close buttons) for the terminal screenshot.
- Cost savings annotation on the aggregate chart (e.g., "Save 92.3%").
- README layout: banner on top, then terminal output, then cost charts, then existing content.

## Constraints
- Python 3.10+ only — no external image generation services.
- matplotlib for charts, Pillow for text rendering.
- Dependencies: `matplotlib`, `Pillow`. Both already standard for data science work.
- Images must render correctly in dark and light GitHub README views (use opaque backgrounds, not transparent).
- Images must be under 500KB each.

## Edge Cases
- **User runs script without data/report.txt**: Script should exit with a clear message telling user to run `python run_benchmark.py` first.
- **User runs script without installing Pillow/matplotlib**: Script should import with try/except and print install instructions.
- **Terminal output text is wider than the faux window**: Word-wrap or truncate to fit the window width (80 chars).

## Definition of Done
- `python scripts/generate_readme_images.py` runs without errors and produces 3 PNG files in `docs/images/`.
- README.md has the banner image at top, terminal output image, and cost chart image inserted in order.
- All images display correctly when viewed on GitHub.
- `python -m pytest tests/ -q` still passes (no code changes, only docs/assets).
