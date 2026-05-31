---
name: optimize-latex-tables
description: Generate, repair, compact, validate, and template-fit publication-quality LaTeX tables for papers, journals, conferences, ACM/IEEE/Elsevier-like templates, or user-provided .tex manuscripts. Use when Codex needs to convert CSV, TSV, Excel, JSON, or existing LaTeX tabular data into a directly usable table; preserve original data values; infer target template constraints; apply conservative best/second-best highlighting; produce package notes and manifests; compile previews; audit readability and data integrity.
---

# Optimize LaTeX Tables

## Activation

Classify the request before acting:

- `generate`: source data plus a paper/template `.tex` -> new table.
- `repair`: existing LaTeX table -> cleaner equivalent with the same data.
- `fit`: table is too wide, dense, or unreadable in a target template.
- `audit`: check a table for data drift, package needs, and readability risks.
- `triage`: inspect a manuscript/template and explain table constraints.

For `generate`, `repair`, and `fit`, use the bundled script. Do not rely only on manual editing when a source data file exists.

## Required Workflow

1. Resolve the skill root and run scripts from this skill bundle, not from the target paper directory.
2. Inspect the target `.tex` with `analyze-template`; treat it as the layout authority.
3. Ingest source data with `ingest`; keep `table_data.json` and its fingerprint.
4. Read only the references needed for the current case:
   - `references/input-contracts.md` for accepted inputs, headers, sheets, and value preservation.
   - `references/table-spec.md` for explicit grouping, comparison scopes, metric directions, and notes.
   - `references/table-design-rules.md` for layout, width, grouping, captions, and split decisions.
   - `references/highlight-policy.md` before applying automatic emphasis.
   - `references/template-detection.md` for venue/template adaptation.
   - `references/quality-gates.md` before returning a final answer.
   - `references/workflow-recipes.md` for common command recipes.
5. Generate the table and manifest.
6. Run `validate` and `audit`.
7. Run `preview` when a target `.tex` is available, then inspect the PDF or rendered PNG.
8. Return the table, required package additions, validation/audit status, and any unresolved risks.

## Script Commands

Prefer `build` when the user provides both source data and a target paper/template:

```bash
python scripts/table_pipeline.py build --paper paper.tex --input data.csv --caption "Results" --label "tab:results" --outdir table-build
```

`build` writes `template_profile.json`, `table_data.json`, `table.tex`, `generation_manifest.json`, `validation.json`, `audit.json`, optional preview artifacts, and `build_summary.json`.

Use the lower-level commands when debugging or when the user asks for a specific stage:

```bash
python scripts/table_pipeline.py analyze-template --tex paper.tex --out template_profile.json
python scripts/table_pipeline.py ingest --input data.csv --out table_data.json
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Results" --label "tab:results" --out table.tex
python scripts/table_pipeline.py validate --data table_data.json --table table.tex --report validation.json
python scripts/table_pipeline.py audit --table table.tex --template template_profile.json --report audit.json
python scripts/table_pipeline.py preview --paper paper.tex --table table.tex --outdir preview
```

Useful options:

- `ingest --sheet "Sheet1" --header-row 2` for Excel or non-first-row headers.
- `build --skip-preview` when Tectonic preview is impossible or too slow.
- `generate --metric-directions "Accuracy=higher,Loss=lower,Params=none"` for explicit emphasis rules.
- `generate --config table_spec.json` for grouped headers, notes, row grouping, and compare-within-dataset rules.
- `generate --no-highlight` for strict black-and-white data display.
- `generate --no-second-best` when only the best value should be emphasized.
- `generate --wide yes|no|auto` to control `table*`.
- `generate --style journal|blackwhite|compact` to control conservative density choices.

## Hard Rules

- Never change, round, remove, reorder, or relabel data values unless the user explicitly requests that transformation.
- Preserve a machine-readable source artifact (`table_data.json`) and a generation manifest.
- Prefer the `build` command for end-to-end work so validation, audit, and preview reports are produced together.
- Do not guess metric direction when it can affect a scientific claim.
- Use an explicit table spec for complex tables with grouped headers, dataset/task-specific comparisons, row groups, or table notes.
- For README/project-page images, use presentation-surface styling guidance from `references/table-design-rules.md` and the `sage`, `blue`, or `lavender` theme guidance in `references/table-spec.md`.
- Prefer structural readability over shrinking a table until it technically fits.
- Add only packages required by the generated table; report them explicitly.
- If validation fails, do not present the table as final.
- If full-manuscript compilation fails for unrelated reasons, preview in a temporary minimal document and disclose that limitation.

## Output Contract

When returning final work, include:

- path to the generated `.tex`
- required package additions, if any
- validation result and mismatch count
- audit result and important findings
- preview PDF/PNG path when available
- concise notes for any manual decision still required, especially ambiguous metric direction or strict publisher package limits
