# Input Contracts

Use this reference before ingesting data or promising data preservation.

## Supported Inputs

- CSV: first row is the header by default; use `--header-row` for other layouts.
- TSV: same as CSV but tab-delimited.
- XLSX: active sheet by default; use `--sheet` to select a named sheet.
- JSON: either `{ "columns": [...], "rows": [...] }`, a list of objects, or a list of row arrays.
- LaTeX: standard `tabular`, `tabularx`, or `tabular*` inside or outside a `table` float.

Unsupported inputs should be converted to one of these formats before generation.

## Preservation Rules

- Treat cell strings as authoritative after ingestion.
- Preserve visible decimals and percentages from Excel number formats when possible.
- Preserve percent signs, uncertainty notation, plus/minus markers, arrows, and text notes.
- Escape LaTeX special characters only as a display operation.
- Do not infer missing values, merge cells, or drop rows.
- Do not convert units unless the user explicitly asks for a transformed display.

## Headers

- Headers are display labels and comparison scopes.
- Multi-level headers in spreadsheets should be flattened only when the user provides or accepts a flattening rule.
- For existing LaTeX tables with `\multicolumn` or `\multirow`, preserve visible text and warn that spanning semantics may need manual review.

## Safe Normalization

The script may normalize for validation by removing formatting wrappers such as `\textbf{}` and `\underline{}`. That normalization is only for comparison; it must not be used to rewrite the source data.

## When To Ask

Ask for clarification before final generation when:

- the header row is unclear
- multiple Excel sheets look plausible
- multi-level headers need semantic grouping
- metric direction affects highlighting and cannot be inferred safely
- the target publisher appears to ban extra packages
