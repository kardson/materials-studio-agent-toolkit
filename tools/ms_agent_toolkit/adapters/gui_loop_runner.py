from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.ms_bridge.scripts.write_run_result import build_run_result, write_run_result
from tools.ms_bridge.scripts.write_task_manifest import write_manifest


def enqueue_gui_loop_job(
    *,
    queue_root: Path,
    workspace_root: Path,
    job_name: str,
    rendered_script: str,
    manifest: dict,
) -> dict:
    queue_root = Path(queue_root)
    workspace_root = Path(workspace_root)
    pending_dir = queue_root / "pending"
    logs_dir = queue_root / "logs"
    pending_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    workspace_root.mkdir(parents=True, exist_ok=True)

    script_path = workspace_root / job_name
    script_path.write_text(rendered_script, encoding="utf-8")
    queued_script_path = pending_dir / job_name
    shutil.copy2(script_path, queued_script_path)

    manifest_path = write_manifest(workspace_root / "task_manifest.json", manifest)
    run_result = build_run_result(
        ok=True,
        script_path=str(queued_script_path),
        result_dir=manifest["resultDir"],
        gui_visible_mode="gui_loop",
        known_files=[str(queued_script_path), str(logs_dir / f"{job_name}.status.json")],
        error=None,
    )
    run_result_path = write_run_result(workspace_root / "run_result.json", run_result)
    return {
        "stage": "task_queued",
        "scriptPath": str(queued_script_path),
        "manifestPath": str(manifest_path),
        "runResultPath": str(run_result_path),
    }


def read_gui_loop_job_state(queue_root: Path, job_name: str) -> dict:
    queue_root = Path(queue_root)
    status_path = queue_root / "logs" / f"{job_name}.status.json"
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))
        return {
            "state": "completed" if status.get("ok") else "failed",
            "ok": bool(status.get("ok")),
            "stdoutPath": status.get("stdout_file"),
            "error": status.get("error_message"),
            "statusPath": str(status_path),
        }

    if (queue_root / "pending" / job_name).exists():
        state = "queued"
    elif (queue_root / "running" / job_name).exists():
        state = "running"
    elif (queue_root / "done" / job_name).exists():
        state = "completed"
    elif (queue_root / "failed" / job_name).exists():
        state = "failed"
    else:
        state = "missing"

    return {
        "state": state,
        "ok": state == "completed",
        "stdoutPath": None,
        "error": None,
        "statusPath": str(status_path),
    }
