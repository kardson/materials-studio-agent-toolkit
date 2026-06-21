from __future__ import annotations

from pathlib import Path

from tools.ms_bridge.scripts.read_castep_result import parse_castep_bundle


def parse_result_dir(result_dir: Path) -> dict:
    result_dir = Path(result_dir)
    castep = result_dir / "sample.castep"
    param = result_dir / "sample.param"
    summary = result_dir / "sample_summary.txt"
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
            "summaryPath": str(summary),
        },
        "error": None,
    }
