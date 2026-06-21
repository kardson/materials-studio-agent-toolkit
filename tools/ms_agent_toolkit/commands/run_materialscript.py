from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.adapters.materialscript_runner import build_backend_contract
from tools.ms_agent_toolkit.capabilities import CapabilityRegistry


def build_compliant_request(capability_id: str, params_json: str) -> dict:
    parameters = json.loads(params_json)
    registry = CapabilityRegistry(Path(__file__).resolve().parents[1] / "capabilities")
    capability = registry.get(capability_id)
    unsupported = sorted(set(parameters) - set(capability["allowed_parameters"]))
    if unsupported:
        raise ValueError(f"Unsupported parameters for {capability_id}: {', '.join(unsupported)}")
    missing = [name for name in capability["required_inputs"] if name not in parameters]
    if missing:
        raise ValueError(f"Missing required parameters for {capability_id}: {', '.join(missing)}")

    input_document = str(parameters["input_xsd"])
    script_path = str(Path(input_document).with_suffix(".pl"))
    result_dir = str(Path(input_document).with_suffix(""))
    return {
        "mode": "compliant",
        "capabilityId": capability_id,
        "module": capability["module"],
        "task": capability["task"],
        "templateId": capability["template_id"],
        "parameters": parameters,
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
            parameters=parameters,
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capability", required=True)
    parser.add_argument("--params-json", required=True)
    args = parser.parse_args()
    print(json.dumps(build_compliant_request(args.capability, args.params_json), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
