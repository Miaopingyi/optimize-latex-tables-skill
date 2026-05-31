# Highlight Policy

Automatic highlighting must be conservative. The goal is to help readers find the main result without overstating ambiguous comparisons.

## Metric Direction

Infer "higher is better" only for clear names such as:

- accuracy, acc, f1, auc, auroc, auprc, precision, recall
- score, performance, success, pass rate
- bleu, rouge, meteor, cider, map, ndcg

Infer "lower is better" only for clear names such as:

- loss, error, err, mae, mse, rmse, mape
- perplexity, ppl, wer, cer
- latency, time, memory, cost, params, flops

Do not infer direction for ambiguous names such as `value`, `rate`, `delta`, `change`, `gap`, `ratio`, `mean`, `std`, or custom abbreviations.

## Comparison Groups

- Compare within a column by default.
- Use table spec `compare_by` for dataset/task/model-family scoped comparisons.
- If headers define datasets, tasks, or metric families, compare only within the same metric and same dataset/task group.
- Do not compare aggregate rows against subgroup rows unless the user says they are comparable.
- Do not compare values with incompatible units or different arrows.
- Do not compare results across different training data, parameter budgets, or prompt settings unless the table explicitly treats them as one leaderboard.
- If standard deviation or confidence intervals are present, preserve them and avoid significance claims unless the user provides a statistical rule.

## Visual Encoding

- Best unambiguous value: `\textbf{...}`.
- Second-best unambiguous value: `\underline{...}`.
- Significant result already marked in the source: preserve the source marker.
- Header or panel emphasis: shallow gray background such as `gray!10` only when `xcolor[table]` is available or acceptable.
- For strict black-and-white venues, use only `\textbf{}` and optionally `\underline{}`.
- Do not combine bold, underline, color, and symbols in one cell unless the source already uses a symbol with defined meaning.

Avoid saturated colors, red/green semantics, and multiple simultaneous encodings in the same cell.

## Failure Mode

If metric direction or comparison grouping is not clear, leave values unhighlighted and ask for a short rule such as:

```text
For Accuracy/F1/AUC higher is better; for Loss/RMSE lower is better; compare methods within each dataset.
```

Never guess when a wrong highlight could change the paper's scientific claim.

## User-Provided Rules

Prefer explicit rules when the table is high-stakes or custom:

```text
Compare methods within each dataset block. Accuracy, F1, and AUC are higher-is-better. Loss, RMSE, latency, and parameters are lower-is-better. Do not highlight the "Delta" column.
```

Pass simple overrides to the script with:

```bash
--metric-directions "Accuracy=higher,F1=higher,Loss=lower,Delta=none"
```
