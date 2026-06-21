from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_manifest(
    task_id: str,
    task_type: str,
    input_document: str,
    output_document: str,
    result_dir: str,
    classification: str,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    return {
        "taskId": task_id,
        "taskType": task_type,
        "inputDocument": input_document,
        "outputDocument": output_document,
        "resultDir": result_dir,
        "classification": classification,
        "parameters": parameters,
        "createdAt": utc_now_iso(),
    }


def write_manifest(output_file: Path, manifest: dict[str, Any]) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a task_manifest.json file.")
    parser.add_argument("--output", required=True, help="Output manifest path")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-type", required=True)
    parser.add_argument("--input-document", required=True)
    parser.add_argument("--output-document", required=True)
    parser.add_argument("--result-dir", required=True)
    parser.add_argument("--classification", choices=["production", "diagnostic"], required=True)
    parser.add_argument(
        "--parameters-json",
        default="{}",
        help="JSON object string containing task parameters",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parameters = json.loads(args.parameters_json)
    manifest = build_manifest(
        task_id=args.task_id,
        task_type=args.task_type,
        input_document=args.input_document,
        output_document=args.output_document,
        result_dir=args.result_dir,
        classification=args.classification,
        parameters=parameters,
    )
    path = write_manifest(Path(args.output), manifest)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
