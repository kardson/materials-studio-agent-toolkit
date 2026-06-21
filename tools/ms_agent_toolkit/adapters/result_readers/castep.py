from __future__ import annotations

from pathlib import Path

from tools.ms_bridge.scripts.read_castep_result import parse_castep_bundle


def _discover_single(result_dir: Path, pattern: str, label: str) -> Path:
    matches = sorted(result_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Missing {label} file in {result_dir}")
    return matches[0]


def parse_result_dir(result_dir: Path) -> dict:
    result_dir = Path(result_dir)
    castep = _discover_single(result_dir, "*.castep", "CASTEP result")
    param = _discover_single(result_dir, "*.param", "CASTEP parameter")
    summary_matches = sorted(result_dir.glob("*summary*.txt"))
    summary = summary_matches[0] if summary_matches else None
    parsed = parse_castep_bundle(castep, param, summary)
    return {
        "ok": True,
        "stage": "result_parsed",
        "mode": "generic",
        "capabilityId": None,
        "result": parsed,
        "evidence": {
            "castepPath": str(castep),
            "paramPath": str(param),
            "summaryPath": str(summary) if summary else None,
        },
        "error": None,
    }
