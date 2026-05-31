# Optimize LaTeX Tables Skill

`optimize-latex-tables` is a Codex skill for generating publication-ready LaTeX tables from CSV, TSV, Excel, JSON, or existing LaTeX table sources. It is designed for paper-writing workflows where the final table must fit a target conference or journal template, preserve the original data, and pass repeatable validation before use.

## What It Does

- Converts structured data or existing `tabular` sources into clean LaTeX tables.
- Adapts table layout to a target manuscript/template `.tex` file.
- Preserves source values through a normalized `table_data.json` fingerprint.
- Applies conservative best/second-best highlighting with explicit metric rules.
- Supports grouped headers, per-dataset comparisons, row grouping, and table notes through `table_spec.json`.
- Produces validation, audit, manifest, and preview reports for reproducible use.
- Compiles a preview with Tectonic when available and records PDF/PNG artifacts.

## Repository Layout

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── highlight-policy.md
│   ├── input-contracts.md
│   ├── quality-gates.md
│   ├── table-design-rules.md
│   ├── table-spec.md
│   ├── template-detection.md
│   └── workflow-recipes.md
└── scripts/
    ├── table_pipeline.py
    └── smoke_test.py
```

## Quick Start

Run the end-to-end build command when you have both a data file and a target paper template:

```bash
python scripts/table_pipeline.py build \
  --paper paper.tex \
  --input results.csv \
  --caption "Main results." \
  --label "tab:main-results" \
  --outdir table-build
```

The build command writes:

- `template_profile.json`
- `table_data.json`
- `table.tex`
- `generation_manifest.json`
- `validation.json`
- `audit.json`
- `preview.json` when preview succeeds
- `build_summary.json`

## Complex Tables

Use `table_spec.json` for grouped headers and scoped comparisons:

```json
{
  "metric_directions": {
    "Accuracy": "higher",
    "Loss": "lower"
  },
  "compare_by": ["Dataset"],
  "row_group_by": ["Dataset"],
  "column_groups": [
    {"label": "Setup", "columns": ["Dataset", "Method"]},
    {"label": "Metrics", "columns": ["Accuracy", "Loss"]}
  ],
  "notes": ["Bold indicates best within each dataset."]
}
```

Then run:

```bash
python scripts/table_pipeline.py build \
  --paper paper.tex \
  --input grouped-results.csv \
  --caption "Grouped results." \
  --label "tab:grouped-results" \
  --outdir grouped-build \
  --config table_spec.json
```

## Lower-Level Commands

The pipeline can also be run stage by stage:

```bash
python scripts/table_pipeline.py analyze-template --tex paper.tex --out template_profile.json
python scripts/table_pipeline.py ingest --input results.csv --out table_data.json
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Results." --label "tab:results" --out table.tex
python scripts/table_pipeline.py validate --data table_data.json --table table.tex --report validation.json
python scripts/table_pipeline.py audit --table table.tex --template template_profile.json --report audit.json
python scripts/table_pipeline.py preview --paper paper.tex --table table.tex --outdir preview --report preview.json
```

## Quality Gates

A table should not be treated as final unless:

- `validate` returns `ok: true`.
- `audit` has no blocking errors.
- Required packages are listed in the manifest or table comments.
- The preview PDF/PNG has been inspected when a target `.tex` file is available.
- Ambiguous metric direction has been resolved explicitly or left unhighlighted.

## Testing

Run the smoke test:

```bash
python scripts/smoke_test.py
```

The smoke test covers one-command builds, CSV, TSV, JSON, XLSX when `openpyxl` is available, existing LaTeX input, grouped headers, scoped highlighting, validation failure behavior, audit behavior, and preview when rendering tools are available.

## Requirements

- Python 3.10+
- Optional: `openpyxl` for `.xlsx` input
- Optional: `Pillow` for PNG preview analysis
- Optional: Tectonic and `pdftoppm` for PDF/PNG preview generation

The core CSV/TSV/JSON/LaTeX flows use the Python standard library.

## Installing As A Codex Skill

Copy this folder to your Codex skills directory:

```text
%USERPROFILE%\.codex\skills\optimize-latex-tables
```

Then invoke it as:

```text
$optimize-latex-tables
```

## License

MIT License. See [LICENSE](LICENSE).
