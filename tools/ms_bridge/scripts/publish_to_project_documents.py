from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_publish_manifest(
    input_path: str,
    target_documents_dir: str,
    output_name: str,
    classification: str,
) -> dict[str, Any]:
    target_dir = Path(target_documents_dir)
    output_path = target_dir / output_name
    return {
        "action": "publish_to_project_documents",
        "inputPath": input_path,
        "targetDocumentsDir": str(target_dir),
        "outputName": output_name,
        "outputPath": str(output_path),
        "classification": classification,
        "createdAt": utc_now_iso(),
    }


def write_manifest(output_file: Path, payload: dict[str, Any]) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_file


def build_publish_summary(
    manifest_path: str,
    run_result_path: str,
    bridge_response: dict[str, Any],
) -> dict[str, Any]:
    stdout = str(bridge_response.get("nativeStdout", ""))
    stdout_lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    published_path = stdout_lines[-1] if stdout_lines else None
    return {
        "ok": bool(bridge_response.get("ok", False)),
        "manifestPath": manifest_path,
        "runResultPath": run_result_path,
        "publishedPath": published_path,
        "nativeLogPath": bridge_response.get("nativeLogPath"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a publish-to-project-documents manifest.")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--target-documents-dir", required=True)
    parser.add_argument("--output-name", required=True)
    parser.add_argument("--classification", choices=["production", "diagnostic"], required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run", action="store_true", help="Run the publish action through invoke_materialscript.ps1")
    parser.add_argument("--runmatscript-bat", default=None)
    parser.add_argument("--invoke-script", default=None)
    parser.add_argument("--template-script", default=None)
    parser.add_argument("--run-result-output", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = build_publish_manifest(
        input_path=args.input_path,
        target_documents_dir=args.target_documents_dir,
        output_name=args.output_name,
        classification=args.classification,
    )
    manifest_path = write_manifest(Path(args.output), payload)
    if not args.run:
      print(manifest_path)
      return 0

    if not args.runmatscript_bat or not args.invoke_script or not args.template_script or not args.run_result_output:
      raise SystemExit("--run requires --runmatscript-bat, --invoke-script, --template-script, and --run-result-output")

    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        (
            f"& '{args.invoke_script}' "
            f"-RunMatScriptBat '{args.runmatscript_bat}' "
            f"-ScriptPath '{args.template_script}' "
            f"-ScriptArguments @('{args.input_path}','{args.target_documents_dir}','{args.output_name}') "
            f"-AsJson"
        ),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    bridge_response = json.loads(completed.stdout)

    run_result_path = Path(args.run_result_output)
    run_result_path.parent.mkdir(parents=True, exist_ok=True)
    run_result_path.write_text(json.dumps(bridge_response, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = build_publish_summary(
        manifest_path=str(manifest_path),
        run_result_path=str(run_result_path),
        bridge_response=bridge_response,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
