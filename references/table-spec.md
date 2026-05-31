# Table Spec JSON

Use a table spec when the table needs decisions that should be explicit and reproducible. Keep the spec small and local to the generated table.

## Supported Fields

```json
{
  "metric_directions": {
    "Accuracy": "higher",
    "Loss": "lower",
    "Params": "none"
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

## Semantics

- `metric_directions`: explicit higher/lower/none rules. These override automatic inference.
- `compare_by`: compare best and second-best values within each group defined by these columns.
- `row_group_by`: preserve all rows and values, but add visual spacing when the group changes.
- `column_groups`: add a grouped header row with `\multicolumn`. Groups must be contiguous and non-overlapping.
- `notes`: add compact table notes below the tabular environment.

## Safety Rules

- Do not use a spec to silently relabel, round, sort, or remove data.
- Use `compare_by` for dataset/task-specific leaderboards; otherwise a method can be incorrectly highlighted across incomparable groups.
- Use `metric_directions` whenever metric names are custom or ambiguous.
- Validate after generation; grouped headers are display structure and must not alter the data rows.

## Command

```bash
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Results." --label "tab:results" --out table.tex --config table_spec.json
```
