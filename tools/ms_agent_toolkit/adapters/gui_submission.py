from __future__ import annotations


def build_gui_manifest(capability_id: str, input_xsd: str, output_dir: str) -> dict:
    return {
        "ok": True,
        "stage": "script_generated",
        "mode": "compliant",
        "capabilityId": capability_id,
        "error": None,
        "evidence": {
            "xsdPath": input_xsd,
            "manifestPath": f"{output_dir}/task_manifest.json",
            "plPath": f"{output_dir}/job.pl",
            "readmePath": f"{output_dir}/README.md",
        },
    }
