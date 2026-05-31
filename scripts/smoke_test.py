#!/usr/bin/env python3
"""Run regression smoke tests for the optimize-latex-tables skill."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=str(cwd), text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    return result


def write(path: Path, text: str) -> None:
    path.write_text(text.strip() + "\n", encoding="utf-8")


def main() -> None:
    skill_root = Path(__file__).resolve().parents[1]
    pipeline = skill_root / "scripts" / "table_pipeline.py"
    python = sys.executable
    with tempfile.TemporaryDirectory(prefix="optimize-latex-tables-") as tmp:
        root = Path(tmp)
        write(
            root / "paper.tex",
            r"""
            \documentclass[sigconf]{acmart}
            \usepackage{booktabs}
            \begin{document}
            Smoke.
            \end{document}
            """,
        )
        write(
            root / "data.csv",
            """Method,Accuracy,Loss,Ambiguous
            Base,81.2,0.42,5
            Ours,84.7,0.31,7
            Alt,83.1,0.37,6""",
        )
        write(
            root / "grouped.csv",
            """Dataset,Method,Accuracy,Loss
            A,Base,81.2,0.42
            A,Ours,84.7,0.31
            B,Base,78.0,0.48
            B,Ours,80.3,0.45""",
        )
        write(
            root / "table_spec.json",
            json.dumps(
                {
                    "metric_directions": {"Accuracy": "higher", "Loss": "lower"},
                    "compare_by": ["Dataset"],
                    "row_group_by": ["Dataset"],
                    "column_groups": [
                        {"label": "Setup", "columns": ["Dataset", "Method"]},
                        {"label": "Metrics", "columns": ["Accuracy", "Loss"]},
                    ],
                    "notes": ["Bold indicates best within each dataset."],
                }
            ),
        )
        write(
            root / "data.tsv",
            "Method\tF1\tRMSE\nA\t72.4\t3.1\nB\t75.2\t2.8\nC\t74.0\t2.9",
        )
        write(
            root / "data.json",
            json.dumps(
                [
                    {"Method": "A", "AUC": "90.1", "Cost": "11"},
                    {"Method": "B", "AUC": "91.0", "Cost": "9"},
                    {"Method": "C", "AUC": "90.5", "Cost": "10"},
                ]
            ),
        )
        try:
            from openpyxl import Workbook

            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Main"
            sheet.append(["Method", "F1", "RMSE"])
            sheet.append(["A", 72.4, 3.1])
            sheet.append(["B", 75.2, 2.8])
            sheet.append(["C", 74.0, 2.9])
            for row in sheet.iter_rows(min_row=2, min_col=2, max_col=3):
                for cell in row:
                    cell.number_format = "0.0"
            workbook.save(root / "data.xlsx")
            inputs = ["data.csv", "data.tsv", "data.json", "data.xlsx", "existing.tex"]
        except ImportError:
            inputs = ["data.csv", "data.tsv", "data.json", "existing.tex"]
        write(
            root / "existing.tex",
            r"""
            \begin{table}[t]
            \centering
            \caption{Existing}
            \label{tab:existing}
            \begin{tabular}{lcc}
            \toprule
            Method & Accuracy & Loss \\
            Base & 81.2 & 0.42 \\
            Ours & 84.7 & 0.31 \\
            \bottomrule
            \end{tabular}
            \end{table}
            """,
        )
        run([python, str(pipeline), "analyze-template", "--tex", "paper.tex", "--out", "template.json"], root)
        run(
            [
                python,
                str(pipeline),
                "build",
                "--paper",
                "paper.tex",
                "--input",
                "grouped.csv",
                "--caption",
                "One command grouped smoke",
                "--label",
                "tab:build-grouped",
                "--outdir",
                "build-output",
                "--config",
                "table_spec.json",
                "--skip-preview",
            ],
            root,
        )
        if not (root / "build-output" / "build_summary.json").exists():
            raise SystemExit("build command did not write build_summary.json")
        run([python, str(pipeline), "ingest", "--input", "grouped.csv", "--out", "grouped.table_data.json"], root)
        run(
            [
                python,
                str(pipeline),
                "generate",
                "--data",
                "grouped.table_data.json",
                "--template",
                "template.json",
                "--caption",
                "Grouped smoke",
                "--label",
                "tab:grouped",
                "--out",
                "grouped.table.tex",
                "--config",
                "table_spec.json",
            ],
            root,
        )
        run([python, str(pipeline), "validate", "--data", "grouped.table_data.json", "--table", "grouped.table.tex"], root)
        run([python, str(pipeline), "audit", "--table", "grouped.table.tex", "--template", "template.json"], root)
        for stem in inputs:
            input_path = root / stem
            safe_name = input_path.name.replace(".", "_")
            out_data = root / f"{safe_name}.table_data.json"
            out_tex = root / f"{safe_name}.table.tex"
            ingest = [python, str(pipeline), "ingest", "--input", str(input_path), "--out", str(out_data)]
            if input_path.suffix == ".xlsx":
                ingest.extend(["--sheet", "Main"])
            run(ingest, root)
            run(
                [
                    python,
                    str(pipeline),
                    "generate",
                    "--data",
                    str(out_data),
                    "--template",
                    "template.json",
                    "--caption",
                    f"{input_path.stem} smoke",
                    "--label",
                    f"tab:{input_path.stem}",
                    "--out",
                    str(out_tex),
                ],
                root,
            )
            run([python, str(pipeline), "validate", "--data", str(out_data), "--table", str(out_tex)], root)
            run([python, str(pipeline), "audit", "--table", str(out_tex), "--template", "template.json"], root)
        changed = root / "changed.tex"
        changed.write_text((root / "data_csv.table.tex").read_text(encoding="utf-8").replace("84.7", "84.8"), encoding="utf-8")
        result = subprocess.run(
            [python, str(pipeline), "validate", "--data", "data_csv.table_data.json", "--table", str(changed)],
            cwd=str(root),
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            raise SystemExit("negative validation did not fail")
        if shutil.which("pdftoppm"):
            run([python, str(pipeline), "preview", "--paper", "paper.tex", "--table", "data_csv.table.tex", "--outdir", "preview"], root)
    print("smoke tests passed")


if __name__ == "__main__":
    main()
