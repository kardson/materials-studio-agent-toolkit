from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_run_result(
    ok: bool,
    script_path: str,
    result_dir: str,
    gui_visible_mode: str,
    known_files: list[str],
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "ok": ok,
        "scriptPath": script_path,
        "resultDir": result_dir,
        "guiVisibleMode": gui_visible_mode,
        "knownFiles": known_files,
        "error": error,
        "updatedAt": utc_now_iso(),
    }


def write_run_result(output_file: Path, run_result: dict[str, Any]) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(run_result, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a run_result.json file.")
    parser.add_argument("--output", required=True, help="Output run result path")
    parser.add_argument("--ok", required=True, choices=["true", "false"])
    parser.add_argument("--script-path", required=True)
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--gui-visible-mode", required=True)
    parser.add_argument("--known-files-json", default="[]", help="JSON string array of file paths")
    parser.add_argument("--error", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    known_files = json.loads(args.known_files_json)
    run_result = build_run_result(
        ok=args.ok.lower() == "true",
        script_path=args.script_path,
        result_dir=args.result_dir,
        gui_visible_mode=args.gui_visible_mode,
        known_files=known_files,
        error=args.error,
    )
    path = write_run_result(Path(args.output), run_result)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
