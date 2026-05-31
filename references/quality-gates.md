# Quality Gates

Use these gates before presenting a table as final.

## Data Integrity

- Prefer `build` for end-to-end final work; it creates a single `build_summary.json`.
- `ingest` completed and wrote `table_data.json`.
- Generated table includes the source fingerprint comment.
- `validate` returns `ok: true`.
- Any display transform is documented in the manifest or final notes.
- Negative checks are trusted: if a manually edited table changes a value, `validate` should fail.

## Template Fit

- `analyze-template` was run on the target `.tex`.
- Required package additions are minimal and listed.
- The chosen float (`table` or `table*`) matches the template column mode.
- The table does not rely on `\resizebox` unless structural alternatives failed.
- Very small fonts are avoided unless the user accepted a compact table.

## Readability

- Header labels are short enough to scan.
- Numeric columns are consistently aligned or at least visually comparable.
- Best/second-best markings are not applied to ambiguous metrics.
- Dataset/task-specific comparisons use `compare_by` or an equivalent explicit rule.
- Grouped headers are contiguous, non-overlapping, and do not hide original columns.
- Captions state the comparison and do not duplicate every header.
- Notes explain metric direction, abbreviations, and significance markers when needed.

## Compilation And Preview

- `preview` compiles with Tectonic when a target `.tex` is available.
- `preview.json` records rendered page paths, LaTeX warnings, and basic PNG image analysis when available.
- Rendered PDF/PNG is visually inspected for width, clipping, unreadable text, and caption/package errors.
- Overfull or LaTeX warnings from the preview log are checked before final delivery.
- If the full manuscript fails for unrelated reasons, the final answer says the preview used a minimal document.

## Final Response

Include only high-signal information:

- generated table path
- package additions
- validation/audit status
- preview artifact path
- unresolved risks or required user choices
