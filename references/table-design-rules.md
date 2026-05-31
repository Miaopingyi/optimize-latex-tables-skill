# Table Design Rules

Use these rules when generating or reshaping LaTeX tables for papers. Keep the source data unchanged and make layout changes explicit.

## Width And Placement

- Follow this fitting ladder before shrinking fonts:
  1. shorten headers and move definitions to notes
  2. use grouped headers and remove repeated words
  3. use `tabularx` for text-heavy columns
  4. reduce `\tabcolsep` modestly
  5. use `table*` in two-column templates
  6. split into semantically meaningful panels
  7. use `adjustbox` with `max width=\linewidth`
  8. consider `resizebox` only as a last resort
- One-column templates: default to `table` and `\columnwidth`.
- Two-column templates: use `table` for narrow tables and `table*` only when the table cannot remain readable in one column.
- Prefer `tabularx` with one or more `X` columns for text-heavy tables.
- Prefer `adjustbox` with `max width=\linewidth` only when column redesign is not enough.
- Avoid `\resizebox{\linewidth}{!}{...}` unless it is the only way to fit a dense numeric table and the preview remains readable.
- If a table needs landscape layout, tell the user; do not add landscape packages silently.

## Complex Headers

- Use grouped headers with `\multicolumn` when columns naturally share a method family, dataset, metric family, or condition.
- Use `references/table-spec.md` and `column_groups` when grouped headers should be generated reproducibly.
- Keep header text short; move repeated units or definitions to captions or notes.
- Put arrows such as `↑` or `↓` in headers only when the target template and font support them; otherwise use `(higher is better)` or `(lower is better)` in a note.
- Rotate headers only for many short metric labels where horizontal text would force unreadable columns.
- Use line breaks in headers only when the template supports them cleanly through `makecell` or `array` column types.

## Rows And Panels

- Preserve source row order unless the user asks for ranking or grouping.
- Use row blocks when the first column contains repeated groups such as dataset, task, model family, or ablation setting.
- Prefer a panel heading row over nested tables.
- Split into multiple tables only when the data has natural semantic groups or the rendered table remains unreadable after compaction.
- For ablations, keep the full model and removals/additions adjacent.
- For method comparisons, keep baselines, prior work, and the proposed method in a consistent order across tables.

## Numeric Alignment

- Align numbers by decimal point when using `siunitx` is already available or explicitly acceptable.
- Otherwise, use centered numeric columns and keep exact source strings.
- Do not round or trim decimals unless the user requests a display precision.
- Keep percent signs, uncertainty intervals, plus/minus notation, and arrows exactly as data semantics require.
- Do not align text notes as numbers. Use a separate note column or table note.

## Captions And Notes

- Captions should state what the table compares, not restate every column.
- Put metric direction hints in captions or notes when they are essential for interpreting highlights.
- Use table notes for abbreviations, statistical significance, or display transforms.
- Do not bury key results in notes; make the table itself readable.

## Minimal Packages

Preferred package order when additions are needed:

```latex
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{adjustbox}
\usepackage[table]{xcolor}
```

Only suggest packages that the generated table actually needs.

## Common Failure Patterns

- Dense result matrices with all metrics repeated for all datasets usually need grouped headers or panels.
- Long method names should be shortened only through user-approved aliases.
- A table that needs both tiny fonts and resizebox should usually be split.
- A table with many colored cells is usually less publication-safe than one with bold/underline and clear grouping.

## Presentation-Surface Styling

For README images, project pages, posters, and slides, a more visual table may be appropriate than the final LaTeX manuscript table.

- Prefer soft backgrounds, rounded outer containers, grouped headers, and muted accent colors.
- Recommended palettes: sage green, pale blue, or lavender.
- Keep values and labels identical to the source data.
- Use the same table specification as the LaTeX output so the visual figure remains traceable.
- Do not use presentation colors as a substitute for validation; still keep `table_data.json`, validation, and audit reports.
