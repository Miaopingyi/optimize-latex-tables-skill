#!/usr/bin/env python3
"""Render polished README table images from the synthetic demo data."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "readme-demo"
ASSETS = ROOT / "assets"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for base in [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")]:
        path = base / name
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_REG = font("segoeui.ttf", 24)
FONT_MED = font("segoeuib.ttf", 24)
FONT_BOLD = font("segoeuib.ttf", 28)
FONT_SMALL = font("segoeui.ttf", 19)
FONT_TINY = font("segoeui.ttf", 17)
FONT_MONO = font("consola.ttf", 18)
FONT_MONO_BOLD = font("consolab.ttf", 18)


THEMES = {
    "sage": {
        "page": "#f5f2ea",
        "card": "#fffdf8",
        "border": "#ddd7cb",
        "title": "#343126",
        "muted": "#928a7d",
        "text": "#3f3a32",
        "line": "#d8d1c4",
        "stripe": "#fbfaf4",
        "best": "#9fe2bf",
        "second": "#dff4e8",
        "emphasis": "#1f3a2d",
    },
    "blue": {
        "page": "#eef4fb",
        "card": "#fbfdff",
        "border": "#cfdbe9",
        "title": "#243348",
        "muted": "#7d8da1",
        "text": "#334155",
        "line": "#c8d5e5",
        "stripe": "#f4f8fd",
        "best": "#a9d6ff",
        "second": "#dcecff",
        "emphasis": "#143b63",
    },
    "lavender": {
        "page": "#f4f1fb",
        "card": "#fffdfd",
        "border": "#dcd3ed",
        "title": "#342945",
        "muted": "#9286a2",
        "text": "#453a52",
        "line": "#d8cfe8",
        "stripe": "#faf7ff",
        "best": "#d5c2ff",
        "second": "#eee6ff",
        "emphasis": "#3a285f",
    },
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return list(rows[0].keys()), rows


def read_spec(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def text_center(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fnt, fill: str) -> None:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = box[0] + (box[2] - box[0] - (bbox[2] - bbox[0])) / 2
    y = box[1] + (box[3] - box[1] - (bbox[3] - bbox[1])) / 2 - 2
    draw.text((x, y), text, font=fnt, fill=fill)


def text_left(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill: str) -> None:
    draw.text(xy, text, font=fnt, fill=fill)


def metric_direction(spec: dict, column: str) -> str | None:
    direction = spec.get("metric_directions", {}).get(column)
    return None if direction == "none" else direction


def numeric(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def compute_rank_styles(columns: list[str], rows: list[dict[str, str]], spec: dict) -> dict[tuple[int, str], str]:
    styles: dict[tuple[int, str], str] = {}
    for col in columns:
        direction = metric_direction(spec, col)
        if direction not in {"higher", "lower"}:
            continue
        values = [(idx, numeric(row[col])) for idx, row in enumerate(rows)]
        values = [(idx, val) for idx, val in values if val is not None]
        if len(values) < 2:
            continue
        ranked = sorted({val for _, val in values}, reverse=(direction == "higher"))
        best = ranked[0]
        second = ranked[1] if len(ranked) > 1 else None
        for idx, val in values:
            if val == best:
                styles[(idx, col)] = "best"
            elif val == second:
                styles[(idx, col)] = "second"
    return styles


def cell_fill(style: str | None, theme: dict[str, str]) -> str:
    if style == "best":
        return theme["best"]
    if style == "second":
        return theme["second"]
    return theme["card"]


def render_table(
    csv_name: str,
    spec_name: str,
    output_name: str,
    title: str,
    subtitle: str,
    theme_name: str = "sage",
) -> None:
    columns, rows = read_csv(DEMO / csv_name)
    spec = read_spec(DEMO / spec_name)
    groups = spec["column_groups"]
    rank_styles = compute_rank_styles(columns, rows, spec)

    width = 1200
    margin = 24
    title_h = 64
    group_h = 48
    header_h = 62
    row_h = 42
    note_h = 48
    height = margin * 2 + title_h + group_h + header_h + len(rows) * row_h + note_h
    theme = THEMES[theme_name]
    image = Image.new("RGB", (width, height), theme["page"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 12, width - 12, height - 12), radius=8, fill=theme["card"], outline=theme["border"], width=1)

    x0 = margin
    y = margin
    table_w = width - margin * 2
    col_w = table_w / len(columns)

    text_center(draw, (margin, y, width - margin, y + 34), title, FONT_BOLD, theme["title"])
    text_center(draw, (margin, y + 32, width - margin, y + title_h), subtitle, FONT_SMALL, theme["muted"])
    y += title_h

    lookup = {col: idx for idx, col in enumerate(columns)}
    for group in groups:
        indices = [lookup[col] for col in group["columns"]]
        gx0 = x0 + min(indices) * col_w
        gx1 = x0 + (max(indices) + 1) * col_w
        text_center(draw, (int(gx0), y, int(gx1), y + 34), group["label"], FONT_MED, theme["title"])
        draw.line((int(gx0) + 12, y + 38, int(gx1) - 12, y + 38), fill=theme["line"], width=2)
    y += group_h

    for idx, col in enumerate(columns):
        x = x0 + idx * col_w
        label = col.replace(" ", "\n") if len(col) > 11 else col
        text_center(draw, (int(x), y, int(x + col_w), y + header_h), label, FONT_REG, theme["text"])
    y += header_h
    draw.line((margin, y, width - margin, y), fill=theme["line"], width=2)

    for row_idx, row in enumerate(rows):
        row_y = y + row_idx * row_h
        if row_idx % 2 == 1:
            draw.rectangle((margin, row_y, width - margin, row_y + row_h), fill=theme["stripe"])
        for col_idx, col in enumerate(columns):
            x = x0 + col_idx * col_w
            style = rank_styles.get((row_idx, col))
            if style:
                draw.rectangle((int(x), row_y, int(x + col_w), row_y + row_h), fill=cell_fill(style, theme))
            value = row[col]
            fnt = FONT_MED if style == "best" else FONT_REG
            fill = theme["emphasis"] if style else theme["text"]
            if col_idx == 0:
                text_left(draw, (int(x) + 12, row_y + 8), value, fnt if style == "best" else FONT_MED, fill)
            else:
                text_center(draw, (int(x), row_y, int(x + col_w), row_y + row_h), value, fnt, fill)
        draw.line((margin, row_y + row_h, width - margin, row_y + row_h), fill=theme["line"])
    y += len(rows) * row_h
    draw.line((margin, y, width - margin, y), fill=theme["title"], width=3)

    note = " ".join(spec.get("notes", []))
    text_center(draw, (margin, y + 4, width - margin, y + note_h), note, FONT_TINY, theme["muted"])

    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(ASSETS / output_name)


def render_original(output_name: str) -> None:
    columns, rows = read_csv(DEMO / "llm_benchmark.csv")
    width, height = 1200, 330
    image = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rectangle((12, 12, width - 12, height - 12), outline="#222222", width=1)
    lines = [
        "Prompt: Improve this LLM benchmark table for a paper.",
        "",
        "Original Codex output",
        "",
        " | ".join(columns),
    ]
    for row in rows:
        lines.append(" | ".join(row[col] for col in columns))
    y = 26
    for idx, line in enumerate(lines):
        fnt = FONT_MONO_BOLD if idx in {0, 2, 4} else FONT_MONO
        draw.text((24, y), line, font=fnt, fill="#111111")
        y += 28
    ASSETS.mkdir(parents=True, exist_ok=True)
    image.save(ASSETS / output_name)


def main() -> None:
    render_original("original-codex-table.png")
    render_table(
        "llm_benchmark.csv",
        "llm_benchmark_spec.json",
        "llm-benchmark-table.png",
        "Synthetic LLM Benchmark Comparison",
        "Grouped model setup, reasoning quality, and serving latency",
        "sage",
    )
    render_table(
        "alignment_ablation.csv",
        "alignment_ablation_spec.json",
        "alignment-ablation-table.png",
        "Synthetic Alignment and Retrieval Ablation",
        "Instruction tuning recipe, evaluation quality, and budget",
        "sage",
    )
    render_table(
        "llm_benchmark.csv",
        "llm_benchmark_spec.json",
        "llm-benchmark-table-blue.png",
        "Synthetic LLM Benchmark Comparison",
        "Blue theme variant for README and presentation surfaces",
        "blue",
    )
    render_table(
        "alignment_ablation.csv",
        "alignment_ablation_spec.json",
        "alignment-ablation-table-lavender.png",
        "Synthetic Alignment and Retrieval Ablation",
        "Lavender theme variant for manuscript-facing summaries",
        "lavender",
    )


if __name__ == "__main__":
    main()
