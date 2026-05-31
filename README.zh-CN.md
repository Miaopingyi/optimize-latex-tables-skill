# Optimize LaTeX Tables Skill

`optimize-latex-tables` 是一个面向 Codex 的 LaTeX 表格优化 skill，用于从 CSV、TSV、Excel、JSON 或已有 LaTeX 表格生成可直接用于论文的高质量表格。它重点解决科研写作中的几个核心问题：适配会议/期刊模板、保证原始数据不被改动、自动生成验证报告，并在可能时编译预览。

## 功能概览

- 将结构化数据或已有 `tabular` 表格转换为清晰的 LaTeX 表格。
- 根据目标论文或模板 `.tex` 自动推断版式约束。
- 通过 `table_data.json` 和数据指纹保护原始数据。
- 支持保守的 best / second-best 高亮，并允许显式指定指标方向。
- 支持分组表头、按数据集/任务分组比较、行分组和表注。
- 生成 validation、audit、manifest、preview 等可复现报告。
- 在可用时使用 Tectonic 编译预览，并记录 PDF/PNG 产物。

## 仓库结构

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

## 快速开始

当你同时有数据文件和目标论文模板时，推荐使用一条命令完成完整流程：

```bash
python scripts/table_pipeline.py build \
  --paper paper.tex \
  --input results.csv \
  --caption "Main results." \
  --label "tab:main-results" \
  --outdir table-build
```

该命令会生成：

- `template_profile.json`
- `table_data.json`
- `table.tex`
- `generation_manifest.json`
- `validation.json`
- `audit.json`
- `preview.json`，如果预览成功
- `build_summary.json`

## 复杂表格

如果需要分组表头、按数据集内部比较、行分组或表注，可以使用 `table_spec.json`：

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

然后运行：

```bash
python scripts/table_pipeline.py build \
  --paper paper.tex \
  --input grouped-results.csv \
  --caption "Grouped results." \
  --label "tab:grouped-results" \
  --outdir grouped-build \
  --config table_spec.json
```

## 分步命令

如果需要调试，也可以逐步执行：

```bash
python scripts/table_pipeline.py analyze-template --tex paper.tex --out template_profile.json
python scripts/table_pipeline.py ingest --input results.csv --out table_data.json
python scripts/table_pipeline.py generate --data table_data.json --template template_profile.json --caption "Results." --label "tab:results" --out table.tex
python scripts/table_pipeline.py validate --data table_data.json --table table.tex --report validation.json
python scripts/table_pipeline.py audit --table table.tex --template template_profile.json --report audit.json
python scripts/table_pipeline.py preview --paper paper.tex --table table.tex --outdir preview --report preview.json
```

## 质量门槛

不要在以下条件满足前把表格视为最终版本：

- `validate` 返回 `ok: true`。
- `audit` 没有阻塞错误。
- 所需 LaTeX 包已经在 manifest 或表格注释中列出。
- 如果提供了目标 `.tex`，已检查 preview PDF/PNG。
- 指标方向不明确时，不要擅自高亮；要么显式指定，要么保持不高亮。

## 测试

运行 smoke test：

```bash
python scripts/smoke_test.py
```

该测试覆盖一键 build、CSV、TSV、JSON、可用时的 XLSX、已有 LaTeX 表格、分组表头、分组内高亮、负向数据篡改校验、audit，以及可用时的 preview。

## 依赖

- Python 3.10+
- 可选：`openpyxl`，用于 `.xlsx` 输入
- 可选：`Pillow`，用于 PNG 预览分析
- 可选：Tectonic 和 `pdftoppm`，用于 PDF/PNG 预览

CSV、TSV、JSON 和 LaTeX 的核心流程只依赖 Python 标准库。

## 安装为 Codex Skill

将本目录复制到 Codex skills 目录：

```text
%USERPROFILE%\.codex\skills\optimize-latex-tables
```

然后通过以下方式调用：

```text
$optimize-latex-tables
```

## 许可证

MIT License。见 [LICENSE](LICENSE)。
