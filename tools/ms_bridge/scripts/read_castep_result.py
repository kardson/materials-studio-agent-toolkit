from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FINAL_ENERGY_RE = re.compile(r"Final energy,\s*E\s*=\s*([-\d.]+)", re.IGNORECASE)
FREE_ENERGY_RE = re.compile(r"Final free energy.*?=\s*([-\d.]+)", re.IGNORECASE)
TASK_RE = re.compile(r"task\s*:\s*(\S+)", re.IGNORECASE)
TOTAL_TIME_RE = re.compile(r"Total time\s*=\s*([-\d.]+)\s*s", re.IGNORECASE)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _match_float(pattern: re.Pattern[str], text: str) -> float | None:
    match = pattern.search(text)
    return float(match.group(1)) if match else None


def _match_text(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(1) if match else None


def parse_castep_bundle(castep_file: Path, param_file: Path, summary_file: Path | None = None) -> dict[str, Any]:
    castep_text = _read_text(Path(castep_file))
    param_text = _read_text(Path(param_file))
    summary_text = _read_text(Path(summary_file)) if summary_file else None

    final_energy = _match_float(FINAL_ENERGY_RE, castep_text)
    free_energy = _match_float(FREE_ENERGY_RE, castep_text)
    task = _match_text(TASK_RE, param_text)
    total_time_s = _match_float(TOTAL_TIME_RE, castep_text)

    failed = "electronic_minimisation of initial cell failed" in castep_text.lower()
    completed = final_energy is not None and total_time_s is not None and not failed

    if completed:
        status = "completed"
    elif failed:
        status = "failed"
    else:
        status = "unknown"

    return {
        "status": status,
        "task": task,
        "finalEnergyEv": final_energy,
        "finalFreeEnergyEv": free_energy,
        "totalTimeSeconds": total_time_s,
        "summaryText": summary_text,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read CASTEP result files and return a JSON summary.")
    parser.add_argument("--castep-file", required=True)
    parser.add_argument("--param-file", required=True)
    parser.add_argument("--summary-file", default=None)
    parser.add_argument("--output", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = parse_castep_bundle(
        castep_file=Path(args.castep_file),
        param_file=Path(args.param_file),
        summary_file=Path(args.summary_file) if args.summary_file else None,
    )
    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
        print(args.output)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
