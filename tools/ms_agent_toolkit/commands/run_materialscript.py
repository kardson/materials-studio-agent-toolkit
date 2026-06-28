from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.adapters.gui_loop_runner import enqueue_gui_loop_job
from tools.ms_agent_toolkit.adapters.materialscript_runner import (
    build_backend_contract,
    execute_backend_contract,
)
from tools.ms_agent_toolkit.capabilities import CapabilityRegistry
from tools.ms_agent_toolkit.commands.common import load_params_payload
from tools.ms_agent_toolkit.config import load_config, resolve_config_path
from tools.ms_agent_toolkit.templates import render_template, resolve_template_path


def ensure_execution_ready(capability: dict, backend: str) -> None:
    supported_execution_modes = capability.get("supported_execution_modes", [])
    if backend not in supported_execution_modes:
        raise ValueError(
            f"{capability['capability_id']} is not execution-ready or approved for backend "
            f"'{backend}'; supported execution modes: {supported_execution_modes or 'none'}."
        )


def build_compliant_request(capability_id: str, params_json: str, backend: str = "standalone") -> dict:
    parameters = load_params_payload(params_json=params_json, params_file=None)
    registry = CapabilityRegistry(Path(__file__).resolve().parents[1] / "capabilities")
    capability = registry.get(capability_id)
    execution_mode = "compliant"
    ensure_execution_ready(capability, execution_mode)
    unsupported = sorted(set(parameters) - set(capability["allowed_parameters"]))
    if unsupported:
        raise ValueError(f"Unsupported parameters for {capability_id}: {', '.join(unsupported)}")
    missing = [name for name in capability["required_inputs"] if name not in parameters]
    if missing:
        raise ValueError(f"Missing required parameters for {capability_id}: {', '.join(missing)}")

    input_document = str(parameters["input_xsd"])
    template_parameters = dict(parameters)
    if backend == "gui_loop":
        template_parameters["input_xsd"] = Path(input_document).name
    script_path = str(Path(input_document).with_suffix(".pl"))
    result_dir = str(Path(input_document).with_suffix(""))
    return {
        "mode": "compliant",
        "backend": backend,
        "capabilityId": capability_id,
        "module": capability["module"],
        "task": capability["task"],
        "templateId": capability["template_id"],
        "parameters": template_parameters,
        "backend": build_backend_contract(
            invoke_script=str(
                Path(__file__).resolve().parents[2]
                / "ms_bridge"
                / "scripts"
                / "invoke_materialscript.ps1"
            ),
            runmatscript_bat="RunMatScript.bat",
            script_path=script_path,
            timeout_seconds=1800,
            script_arguments=[input_document],
            input_document=input_document,
            result_dir=result_dir,
            parameters=template_parameters,
        ),
    }


def run_compliant_request(capability_id: str, params_json: str, backend: str = "standalone") -> dict:
    request = build_compliant_request(capability_id, params_json, backend=backend)
    repo_root = Path(__file__).resolve().parents[3]
    toolkit_root = Path(__file__).resolve().parents[1]
    bridge_config_path = resolve_config_path(repo_root / "tools" / "ms_bridge" / "config", "bridge_config")
    toolkit_config_path = resolve_config_path(toolkit_root / "config", "toolkit_config")
    config = load_config(bridge_config_path, toolkit_config_path)

    workspace_root = repo_root / "tools" / "ms_bridge" / "workspace" / request["backend"]["manifest"]["taskId"]
    workspace_root.mkdir(parents=True, exist_ok=True)

    template_path = resolve_template_path(toolkit_root / "templates", request["templateId"])
    rendered_script = render_template(template_path, request["parameters"])
    script_path = workspace_root / f"{request['backend']['manifest']['taskId']}.pl"
    script_path.write_text(rendered_script, encoding="utf-8")

    if backend == "gui_loop":
        queue_result = enqueue_gui_loop_job(
            queue_root=Path(config.gui_loop_queue_root),
            workspace_root=workspace_root,
            job_name=script_path.name,
            rendered_script=rendered_script,
            manifest=request["backend"]["manifest"],
        )
        return {
            "ok": True,
            "stage": queue_result["stage"],
            "mode": request["mode"],
            "backend": "gui_loop",
            "capabilityId": request["capabilityId"],
            "module": request["module"],
            "task": request["task"],
            "templateId": request["templateId"],
            "parameters": request["parameters"],
            "evidence": {
                "scriptPath": str(script_path),
                "queuedScriptPath": queue_result["scriptPath"],
                "manifestPath": queue_result["manifestPath"],
                "runResultPath": queue_result["runResultPath"],
            },
            "error": None,
        }

    backend = dict(request["backend"])
    backend["manifest"] = dict(backend["manifest"])
    backend["manifest"]["resultDir"] = str(workspace_root)
    backend["command"] = backend["command"].replace(
        f"-ScriptPath '{request['backend']['manifest']['inputDocument'].replace('.xsd', '.pl')}'",
        f"-ScriptPath '{script_path}'",
    )
    backend["command"] = backend["command"].replace(
        "RunMatScript.bat",
        config.run_mat_script_bat.replace("'", "''"),
    )

    execution = execute_backend_contract(
        backend=backend,
        manifest_path=workspace_root / "task_manifest.json",
        run_result_path=workspace_root / "run_result.json",
    )

    bridge_response = execution["bridgeResponse"]
    stage = "task_submitted" if "submitted" in str(bridge_response.get("nativeStdout", "")).lower() else "script_executed"
    return {
        "ok": bool(bridge_response.get("ok", False)),
        "stage": stage,
        "mode": request["mode"],
        "capabilityId": request["capabilityId"],
        "module": request["module"],
        "task": request["task"],
        "templateId": request["templateId"],
        "parameters": request["parameters"],
        "evidence": {
            "scriptPath": str(script_path),
            "manifestPath": execution["manifestPath"],
            "runResultPath": execution["runResultPath"],
            "nativeStdoutPath": bridge_response.get("nativeStdoutPath"),
            "nativeLogPath": bridge_response.get("nativeLogPath"),
        },
        "error": None if bridge_response.get("ok", False) else execution["runResult"].get("error"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capability", required=True)
    parser.add_argument("--params-json")
    parser.add_argument("--params-file")
    parser.add_argument("--backend", choices=["standalone", "gui_loop"], default="standalone")
    args = parser.parse_args()
    params_json = json.dumps(
        load_params_payload(
            params_json=args.params_json,
            params_file=args.params_file,
        )
    )
    print(
        json.dumps(
            run_compliant_request(args.capability, params_json, backend=args.backend),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
