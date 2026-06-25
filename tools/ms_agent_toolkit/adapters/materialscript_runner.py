from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.ms_bridge.scripts.write_run_result import build_run_result, write_run_result
from tools.ms_bridge.scripts.write_task_manifest import build_manifest, write_manifest


def build_run_materialscript_command(
    invoke_script: str,
    runmatscript_bat: str,
    script_path: str,
    timeout_seconds: int,
    script_arguments: list[str],
) -> str:
    quoted_args = ",".join(f"'{arg}'" for arg in script_arguments)
    return (
        f"& '{invoke_script}' "
        f"-RunMatScriptBat '{runmatscript_bat}' "
        f"-ScriptPath '{script_path}' "
        f"-TimeoutSeconds {timeout_seconds} "
        f"-ScriptArguments @({quoted_args}) "
        f"-AsJson"
    )


def build_backend_contract(
    *,
    invoke_script: str,
    runmatscript_bat: str,
    script_path: str,
    timeout_seconds: int,
    script_arguments: list[str],
    input_document: str,
    result_dir: str,
    parameters: dict,
) -> dict:
    script_path_obj = Path(script_path)
    manifest = build_manifest(
        task_id=script_path_obj.stem,
        task_type="submit_castep",
        input_document=input_document,
        output_document=str(script_path_obj.with_suffix(".xcd")),
        result_dir=result_dir,
        classification="production",
        parameters=parameters,
    )
    return {
        "manifest": manifest,
        "command": build_run_materialscript_command(
            invoke_script=invoke_script,
            runmatscript_bat=runmatscript_bat,
            script_path=script_path,
            timeout_seconds=timeout_seconds,
            script_arguments=script_arguments,
        ),
    }


def execute_backend_contract(
    *,
    backend: dict,
    manifest_path: Path,
    run_result_path: Path,
) -> dict:
    manifest_file = write_manifest(Path(manifest_path), backend["manifest"])
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        backend["command"],
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    bridge_response = json.loads(completed.stdout)
    run_result = build_run_result(
        ok=bool(bridge_response.get("ok", False)),
        script_path=bridge_response["scriptPath"],
        result_dir=backend["manifest"]["resultDir"],
        gui_visible_mode="standalone",
        known_files=[
            bridge_response.get("nativeStdoutPath"),
            bridge_response.get("nativeLogPath"),
        ],
        error=None if bridge_response.get("ok", False) else "MaterialsScript execution failed",
    )
    run_result_file = write_run_result(Path(run_result_path), run_result)
    return {
        "manifestPath": str(manifest_file),
        "runResultPath": str(run_result_file),
        "bridgeResponse": bridge_response,
        "runResult": run_result,
    }
