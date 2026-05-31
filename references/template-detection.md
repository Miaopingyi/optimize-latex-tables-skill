# Template Detection

Use the user's manuscript or template `.tex` as the layout authority. Inspect local class and style files when they are referenced and available.

## Signals To Extract

- `\documentclass` name and options.
- One-level `\input{...}` and `\include{...}` files when they contain package or macro setup.
- Local `.cls` and `.sty` files referenced by the manuscript when present.
- One-column or two-column mode from class options and class defaults.
- Existing table packages: `booktabs`, `tabularx`, `array`, `adjustbox`, `xcolor`, `colortbl`, `siunitx`, `multirow`, `makecell`, `caption`, `subcaption`.
- Float conventions such as `table`, `table*`, `sidewaystable`, or publisher-specific table macros.
- Existing caption style and label naming patterns.
- Existing use of color or no-color publication constraints.

## Common Defaults

- ACM-like two-column templates: prefer `table` for compact tables and `table*` for wide result matrices; use `booktabs`.
- IEEE-like two-column templates: avoid color by default; use compact headers and readable numeric columns.
- Elsevier-like journal templates: prefer single-column `table` unless the template is explicitly two-column.
- Springer/LNCS-like templates: avoid color and large package additions; compact `booktabs` tables are usually safest.
- NeurIPS/ICLR/ICML-like templates: `booktabs` is usually acceptable; avoid dense color and keep captions concise.
- Unknown class: avoid color, avoid exotic packages, and generate plain `booktabs` LaTeX.

These defaults are fallbacks only. If the provided template contradicts them, follow the template.

## Package Policy

- Reuse packages already loaded by the manuscript.
- Add only the minimal package list needed by the generated table.
- Do not add package options that conflict with existing options.
- If `xcolor` is loaded without `table`, do not rely on `\cellcolor` unless the user accepts changing the package options.
- If the template forbids extra packages, generate plain LaTeX without color or advanced column types.

## Preview Policy

Compile the table in context when possible. If the full manuscript fails for unrelated reasons, build a temporary minimal document that keeps the detected class, options, and required packages, then compile that preview.

Report preview limitations clearly when the temporary document is not identical to the full manuscript.

## Package Conflict Checks

- If `xcolor` is already loaded without `[table]`, do not silently require `\cellcolor`.
- If `caption` is customized by the publisher class, avoid adding caption package options.
- If the class redefines table captions or floats, preserve the class behavior.
- If the template already uses `siunitx`, prefer it for numeric alignment only after checking the version-sensitive syntax in the manuscript.
