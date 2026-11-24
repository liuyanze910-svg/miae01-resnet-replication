"""Aggregate the matched ResNet-20/32 runs and render a dependency-free SVG figure."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, stdev


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "docs" / "results"
OUTPUT = RESULTS / "week4"
PAPER_ERRORS = {20: 8.75, 32: 7.51}
SEEDS = (42, 43, 44)


def load_error(path: Path, expected_depth: int, expected_seed: int) -> float:
    with path.open(encoding="utf-8") as handle:
        summary = json.load(handle)
    test = summary.get("test", {})
    if summary.get("status") != "completed":
        raise ValueError(f"{path}: status is not completed")
    if summary.get("steps") != 16000:
        raise ValueError(f"{path}: expected 16000 steps")
    if summary.get("depth") != expected_depth or summary.get("seed") != expected_seed:
        raise ValueError(f"{path}: depth/seed metadata does not match its path")
    if test.get("samples") != 10000:
        raise ValueError(f"{path}: expected 10000 test samples")
    return float(test["error_pct"])


def load_runs() -> list[dict[str, float | int]]:
    rows = []
    for seed in SEEDS:
        resnet20 = RESULTS / ("week2" if seed == 42 else "week3") / f"resnet20-flip-seed{seed}" / "summary.json"
        resnet32 = RESULTS / ("week2" if seed == 42 else "week3") / f"resnet32-flip-seed{seed}" / "summary.json"
        error20 = load_error(resnet20, 20, seed)
        error32 = load_error(resnet32, 32, seed)
        rows.append(
            {
                "seed": seed,
                "resnet20_test_error_percent": error20,
                "resnet32_test_error_percent": error32,
                "resnet20_minus_resnet32_pp": error20 - error32,
            }
        )
    return rows


def write_csv(rows: list[dict[str, float | int]]) -> None:
    path = OUTPUT / "depth_comparison.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "seed": row["seed"],
                    "resnet20_test_error_percent": f"{row['resnet20_test_error_percent']:.2f}",
                    "resnet32_test_error_percent": f"{row['resnet32_test_error_percent']:.2f}",
                    "resnet20_minus_resnet32_pp": f"{row['resnet20_minus_resnet32_pp']:.2f}",
                }
            )


def write_summary(rows: list[dict[str, float | int]]) -> None:
    errors20 = [float(row["resnet20_test_error_percent"]) for row in rows]
    errors32 = [float(row["resnet32_test_error_percent"]) for row in rows]
    differences = [float(row["resnet20_minus_resnet32_pp"]) for row in rows]
    summary = {
        "protocol": {
            "steps": 16000,
            "test_samples": 10000,
            "seeds": list(SEEDS),
            "augmentation": "horizontal_flip_probability_0.5",
        },
        "resnet20": {
            "paper_test_error_percent": PAPER_ERRORS[20],
            "mean_test_error_percent": mean(errors20),
            "sample_sd_test_error_percent": stdev(errors20),
            "gap_vs_paper_percentage_points": mean(errors20) - PAPER_ERRORS[20],
        },
        "resnet32": {
            "paper_test_error_percent": PAPER_ERRORS[32],
            "mean_test_error_percent": mean(errors32),
            "sample_sd_test_error_percent": stdev(errors32),
            "gap_vs_paper_percentage_points": mean(errors32) - PAPER_ERRORS[32],
        },
        "paired_depth_difference": {
            "definition": "ResNet-20 error minus ResNet-32 error, in percentage points",
            "per_seed_percentage_points": differences,
            "mean_percentage_points": mean(differences),
            "sample_sd_percentage_points": stdev(differences),
            "all_seeds_favor_resnet32": all(value > 0 for value in differences),
            "paper_mean_improvement_percentage_points": PAPER_ERRORS[20] - PAPER_ERRORS[32],
        },
    }
    with (OUTPUT / "depth_comparison_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")


def write_svg(rows: list[dict[str, float | int]]) -> None:
    """Write a small, readable grouped bar chart without a plotting dependency."""
    width, height = 760, 470
    left, right, top, bottom = 78, 28, 38, 78
    plot_width, plot_height = width - left - right, height - top - bottom
    ymax = 12.5

    def y(value: float) -> float:
        return top + plot_height * (1 - value / ymax)

    def esc(value: object) -> str:
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<title>Matched CIFAR-10 test error by ResNet depth</title>',
        '<desc>Three seed-level comparisons of ResNet-20 and ResNet-32 with horizontal flipping.</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#222} .grid{stroke:#d9dee5;stroke-width:1} .axis{stroke:#333;stroke-width:1.2} .bar20{fill:#4472c4} .bar32{fill:#ed7d31} .value{font-size:12px} .label{font-size:13px} .title{font-size:17px;font-weight:700}</style>',
        f'<text x="{width / 2:.1f}" y="23" text-anchor="middle" class="title">Matched test error by depth (16,000 updates)</text>',
    ]
    for tick in range(0, 13, 2):
        yy = y(tick)
        parts.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" class="grid"/>')
        parts.append(f'<text x="{left-10}" y="{yy+4:.1f}" text-anchor="end" class="label">{tick}%</text>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis"/>')
    parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis"/>')
    group_width = plot_width / len(rows)
    bar_width = 46
    for index, row in enumerate(rows):
        center = left + group_width * (index + 0.5)
        for offset, key, class_name in ((-bar_width / 2 - 3, "resnet20_test_error_percent", "bar20"), (3, "resnet32_test_error_percent", "bar32")):
            value = float(row[key])
            x = center + offset
            yy = y(value)
            parts.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{bar_width:.1f}" height="{height-bottom-yy:.1f}" class="{class_name}"/>')
            parts.append(f'<text x="{x+bar_width/2:.1f}" y="{yy-7:.1f}" text-anchor="middle" class="value">{value:.2f}</text>')
        parts.append(f'<text x="{center:.1f}" y="{height-bottom+24}" text-anchor="middle" class="label">Seed {esc(row["seed"])}</text>')
    parts.extend(
        [
            f'<rect x="{width-220}" y="{height-34}" width="14" height="14" class="bar20"/><text x="{width-200}" y="{height-22}" class="label">ResNet-20</text>',
            f'<rect x="{width-108}" y="{height-34}" width="14" height="14" class="bar32"/><text x="{width-88}" y="{height-22}" class="label">ResNet-32</text>',
            '</svg>',
        ]
    )
    (OUTPUT / "depth_comparison.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = load_runs()
    write_csv(rows)
    write_summary(rows)
    write_svg(rows)
    print(f"Validated {len(rows) * 2} runs; wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
