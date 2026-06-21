from __future__ import annotations

import json
from pathlib import Path


def parse_gateway_status(raw: dict) -> dict:
    return {
        "jobId": raw.get("jobId"),
        "status": raw.get("status"),
        "progress": raw.get("progress"),
        "resultsFolder": raw.get("resultsFolder"),
    }


def parse_gateway_status_text(job_id: str, status_text: str) -> dict:
    return {
        "jobId": job_id,
        "status": status_text.strip(),
        "progress": None,
        "resultsFolder": None,
    }


def write_status_json(output_path: str, payload: dict) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)
