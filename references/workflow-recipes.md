# Workflow Recipes

Use these concise recipes for common table tasks.

## CSV To Paper Table

Recommended one-command path:

```bash
python scripts/table_pipeline.py build --paper paper.tex --input results.csv --caption "Main results." --label "tab:main" --outdir table-main
```

Manual staged path:

```bash
python scripts/table_pipeline.py analyze-template --tex paper.tex --out template_profile.json
python scripts/table_pipeline.py ingest --input results.csv --out table_data.json
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Main results." --label "tab:main" --out table_main.tex
python scripts/table_pipeline.py validate --data table_data.json --table table_main.tex --report validation.json
python scripts/table_pipeline.py audit --table table_main.tex --template template_profile.json --report audit.json
python scripts/table_pipeline.py preview --paper paper.tex --table table_main.tex --outdir preview-main
```

## Excel With Non-First Header Row

```bash
python scripts/table_pipeline.py ingest --input results.xlsx --sheet "Main" --header-row 2 --out table_data.json
```

## Explicit Highlight Rules

```bash
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Ablation results." --label "tab:ablation" --out ablation.tex --metric-directions "Accuracy=higher,Loss=lower,Params=none"
```

## Grouped Headers And Per-Dataset Highlights

Create `table_spec.json`:

```json
{
  "metric_directions": {"Accuracy": "higher", "Loss": "lower"},
  "compare_by": ["Dataset"],
  "row_group_by": ["Dataset"],
  "column_groups": [
    {"label": "Setup", "columns": ["Dataset", "Method"]},
    {"label": "Metrics", "columns": ["Accuracy", "Loss"]}
  ],
  "notes": ["Bold indicates best within each dataset."]
}
```

Generate with:

```bash
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Grouped results." --label "tab:grouped" --out grouped.tex --config table_spec.json
```

Or use the one-command path:

```bash
python scripts/table_pipeline.py build --paper paper.tex --input grouped.csv --caption "Grouped results." --label "tab:grouped" --outdir grouped-build --config table_spec.json
```

## Black-And-White Publisher Style

```bash
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Results." --label "tab:results" --out table.tex --style blackwhite --no-second-best
```

## Existing LaTeX Table Repair

```bash
python scripts/table_pipeline.py ingest --input old_table.tex --out table_data.json
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Results." --label "tab:results" --out repaired_table.tex
python scripts/table_pipeline.py validate --data table_data.json --table repaired_table.tex
```

Review warnings carefully when the original table uses `\multicolumn` or `\multirow`; the parser preserves visible text but does not reconstruct complex spanning intent.

## Regression Check For The Skill

```bash
python scripts/smoke_test.py
```

This checks the one-command build path, CSV, TSV, JSON, XLSX when `openpyxl` is available, existing LaTeX input, grouped headers, per-group highlighting, validation failure behavior, audit behavior, and preview when PDF rendering tools are available.
