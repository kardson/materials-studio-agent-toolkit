from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.adapters.result_readers.castep import parse_result_dir


def build_report(module: str, result_dir: str) -> dict:
    if module != "castep":
        raise ValueError("Only castep is supported in the first release.")

    parsed = parse_result_dir(Path(result_dir))
    analysis = parsed["analysis"]
    return {
        "ok": parsed["ok"],
        "stage": "round_report_ready",
        "mode": "generic",
        "module": module,
        "resultDir": str(result_dir),
        "analysis": analysis,
        "archiveRecommendation": {
            "recommended": analysis["status"] == "completed",
            "reason": "Completed results should usually be archived for comparison and traceability."
            if analysis["status"] == "completed"
            else "Do not archive as a final result until the run is completed and interpreted.",
        },
        "nextExecutionPlan": analysis["nextStepOptions"],
        "evidence": parsed["evidence"],
        "result": parsed["result"],
        "error": parsed["error"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--result-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(build_report(args.module, args.result_dir), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
