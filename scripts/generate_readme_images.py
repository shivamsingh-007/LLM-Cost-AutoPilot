"""Generate README images: banner, terminal screenshot, cost charts."""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "data" / "report.txt"
DB_PATH = PROJECT_ROOT / "data" / "llm_autopilot.duckdb"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "images"


def _check_deps():
    missing = []
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        missing.append("matplotlib")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("Pillow")
    try:
        import duckdb  # noqa: F401
    except ImportError:
        missing.append("duckdb")
    if missing:
        print(f"Missing: pip install {' '.join(missing)}")
        sys.exit(1)


def _check_prereqs():
    if not REPORT_PATH.exists():
        print(f"Report not found — run first: python run_benchmark.py")
        sys.exit(1)
    if not DB_PATH.exists():
        print(f"Database not found — run first: python run_benchmark.py")
        sys.exit(1)


def _parse_report():
    text = REPORT_PATH.read_text()
    lines = [l.strip() for l in text.strip().split("\n")]
    total = int(re.search(r"\d+", lines[2]).group())
    reduction = float(re.search(r"[\d.]+", lines[3]).group())
    avg_qual = float(re.search(r"[\d.]+", lines[4]).group())
    qual_pct = float(re.search(r"[\d.]+", lines[5]).group())
    esc = re.search(r"([\d.]+)%", lines[6])
    esc_rate = float(esc.group(1)) if esc else 0
    costs = re.findall(r"[\d.]+", lines[8])
    routed_total = float(costs[0])
    baseline_total = float(costs[1])
    latency = int(re.search(r"\d+", lines[9]).group())
    return {
        "total": total, "reduction": reduction, "avg_quality": avg_qual,
        "quality_parity": qual_pct, "esc_rate": esc_rate,
        "routed_total": routed_total, "baseline_total": baseline_total,
        "latency": latency,
    }


def _get_tier_data():
    import duckdb
    conn = duckdb.connect(str(DB_PATH))
    rows = conn.execute("""
        SELECT complexity_tier,
               ROUND(SUM(cost_usd)::numeric, 4) AS routed_cost,
               ROUND(SUM(baseline_cost_usd)::numeric, 4) AS baseline_cost,
               COUNT(*) AS count
        FROM llm_requests
        GROUP BY complexity_tier
        ORDER BY complexity_tier
    """).fetchall()
    conn.close()
    return rows


# --- BANNER ---

def generate_banner():
    from PIL import Image, ImageDraw, ImageFont

    W, H = 900, 260
    cream = (253, 245, 230)
    dark_brown = (92, 64, 51)
    light_brown = (196, 168, 130)
    light_yellow = (240, 214, 138)

    img = Image.new("RGB", (W, H), cream)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 56)
        sub_font = ImageFont.truetype("arial.ttf", 26)
    except OSError:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    title = "LLM Cost Autopilot"
    b = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((W - (b[2] - b[0])) // 2, 50), title, fill=dark_brown, font=title_font)

    sub = "Intelligent Model Routing System"
    b = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((W - (b[2] - b[0])) // 2, 130), sub, fill=light_brown, font=sub_font)

    draw.rectangle([(270, 115), (630, 118)], fill=light_yellow)

    path = OUTPUT_DIR / "banner.png"
    img.save(path)
    print(f"  Saved {path}")


# --- TERMINAL ---

def generate_terminal():
    from PIL import Image, ImageDraw, ImageFont

    bg = (30, 30, 30)
    text_color = (74, 246, 38)
    bar = (51, 51, 51)

    try:
        font = ImageFont.truetype("consola.ttf", 15)
        fw, fh = font.getbbox("A")[2] - font.getbbox("A")[0], 20
    except OSError:
        font = ImageFont.load_default()
        fw, fh = 8, 16

    pad = 20
    title_h = 32
    dot_r = 5

    report = REPORT_PATH.read_text().strip()
    progress = [
        "Running benchmark on 740 prompts...",
        "  200/740 done...",
        "  400/740 done...",
        "  600/740 done...",
        "  740/740 done...",
    ]
    lines = progress + [""] + report.split("\n")
    max_w = max(len(l) for l in lines)
    max_w = max(max_w, 55)

    W = max_w * fw + pad * 2
    H = len(lines) * fh + pad * 2 + title_h

    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (W, title_h)], fill=bar)
    dots = [(12, 11), (26, 11), (40, 11)]
    dot_colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
    for (dx, dy), dc in zip(dots, dot_colors):
        draw.ellipse([(dx - dot_r, dy - dot_r), (dx + dot_r, dy + dot_r)], fill=dc)

    for i, line in enumerate(lines):
        y = title_h + pad + i * fh
        draw.text((pad, y), line, fill=text_color, font=font)

    path = OUTPUT_DIR / "terminal.png"
    img.save(path)
    print(f"  Saved {path}")


# --- COST CHARTS ---

def generate_cost_charts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    cream = "#FDF5E6"
    light_brown = "#C4A882"
    light_yellow = "#F0D68A"
    dark_brown = "#5C4033"
    warm_white = "#FFF8F0"

    info = _parse_report()
    tier_rows = _get_tier_data()

    tiers = [r[0] for r in tier_rows]
    routed_pt = [float(r[1]) for r in tier_rows]
    baseline_pt = [float(r[2]) for r in tier_rows]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    fig.patch.set_facecolor(cream)

    # Aggregate
    ax1.set_facecolor(cream)
    labels = ["Baseline\n(GPT-4o)", "Routed"]
    vals = [info["baseline_total"], info["routed_total"]]
    bars = ax1.bar(labels, vals, color=[light_brown, light_yellow],
                   edgecolor=dark_brown, linewidth=1.5, width=0.5)

    ax1.text(0.5, info["baseline_total"] * 0.5, f"Save {info['reduction']:.1f}%",
             ha="center", va="center", fontsize=16, fontweight="bold",
             color=dark_brown,
             bbox=dict(boxstyle="round,pad=0.3", facecolor=warm_white, edgecolor=dark_brown))

    for bar, val in zip(bars, vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                 f"${val:.4f}", ha="center", va="bottom", fontsize=12, color=dark_brown)

    ax1.set_ylabel("Total Cost (USD)", fontsize=12, color=dark_brown)
    ax1.set_title(f"Aggregate Cost Comparison ({info['total']} prompts)",
                  fontsize=14, color=dark_brown, fontweight="bold")
    ax1.tick_params(colors=dark_brown)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.4f"))
    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax1.spines[spine].set_color(dark_brown)
    ax1.set_ylim(0, info["baseline_total"] * 1.3)

    # Per-tier
    ax2.set_facecolor(cream)
    x = range(len(tiers))
    w = 0.35

    ax2.bar([i - w / 2 for i in x], baseline_pt, w, label="Baseline (GPT-4o)",
            color=light_brown, edgecolor=dark_brown, linewidth=1)
    ax2.bar([i + w / 2 for i in x], routed_pt, w, label="Routed",
            color=light_yellow, edgecolor=dark_brown, linewidth=1)

    for i, (b, r) in enumerate(zip(baseline_pt, routed_pt)):
        ax2.text(i - w / 2, b + 0.0005, f"${b:.4f}",
                 ha="center", va="bottom", fontsize=9, color=dark_brown, rotation=90)
        ax2.text(i + w / 2, r + 0.0005, f"${r:.4f}",
                 ha="center", va="bottom", fontsize=9, color=dark_brown, rotation=90)

    ax2.set_xticks(list(x))
    ax2.set_xticklabels(tiers, fontsize=12, color=dark_brown)
    ax2.set_ylabel("Cost (USD)", fontsize=12, color=dark_brown)
    ax2.set_title("Per-Tier Cost Breakdown", fontsize=14, color=dark_brown, fontweight="bold")
    ax2.legend(fontsize=10)
    ax2.tick_params(colors=dark_brown)
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.4f"))
    for spine in ["top", "right"]:
        ax2.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax2.spines[spine].set_color(dark_brown)

    plt.tight_layout(pad=3)
    path = OUTPUT_DIR / "cost_chart.png"
    fig.savefig(path, dpi=150, facecolor=cream, edgecolor="none")
    plt.close(fig)
    print(f"  Saved {path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _check_deps()
    _check_prereqs()

    print("Generating README images...")
    generate_banner()
    generate_terminal()
    generate_cost_charts()
    print(f"Done! Images in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
