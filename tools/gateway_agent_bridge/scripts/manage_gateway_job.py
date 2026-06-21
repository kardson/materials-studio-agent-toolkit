from __future__ import annotations

import json
from pathlib import Path


def parse_create_job_stdout(stdout: str) -> dict:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    job_id = lines[-1] if lines else None
    return {
        "jobId": job_id,
        "rawLines": lines,
    }


def parse_simple_ok(action: str, stdout: str) -> dict:
    return {
        "action": action,
        "ok": "Gw-status-code: 600" in stdout or "OK" in stdout,
        "stdout": stdout,
    }


def write_json(output_path: str, payload: dict) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)
