from __future__ import annotations

import shutil
from pathlib import Path

from tools.ms_agent_toolkit.capabilities import CapabilityRegistry
from tools.ms_agent_toolkit.templates import render_template, resolve_template_path
from tools.ms_bridge.scripts.write_task_manifest import build_manifest, write_manifest


def build_gui_manifest(capability_id: str, input_xsd: str, output_dir: str) -> dict:
    output_dir_path = Path(output_dir)
    manifest_path = output_dir_path / "task_manifest.json"
    pl_path = output_dir_path / "job.pl"
    readme_path = output_dir_path / "README.md"
    return {
        "ok": True,
        "stage": "script_generated",
        "mode": "compliant",
        "capabilityId": capability_id,
        "error": None,
        "evidence": {
            "xsdPath": input_xsd,
            "manifestPath": str(manifest_path),
            "plPath": str(pl_path),
            "readmePath": str(readme_path),
        },
    }


def write_gui_package(
    *,
    capability_id: str,
    input_xsd: str,
    output_dir: str,
    parameters: dict,
    template_root: Path,
    capability_root: Path,
) -> dict:
    registry = CapabilityRegistry(capability_root)
    capability = registry.get(capability_id)

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    input_path = Path(input_xsd)
    copied_xsd = output_dir_path / input_path.name
    if input_path.resolve() != copied_xsd.resolve():
        shutil.copy2(input_path, copied_xsd)

    template_path = resolve_template_path(template_root, capability["template_id"])
    rendered = render_template(template_path, parameters)
    pl_path = output_dir_path / "job.pl"
    pl_path.write_text(rendered, encoding="utf-8")

    manifest = build_manifest(
        task_id=output_dir_path.name,
        task_type=capability["task"],
        input_document=copied_xsd.name,
        output_document=capability["template_id"],
        result_dir=str(output_dir_path),
        classification="production",
        parameters=parameters,
    )
    manifest_path = write_manifest(output_dir_path / "task_manifest.json", manifest)

    readme_path = output_dir_path / "README.md"
    readme_path.write_text(
        "\n".join(
            [
                f"# {capability_id}",
                "",
                f"- Input XSD: {copied_xsd.name}",
                f"- Script: {pl_path.name}",
                f"- Manifest: {manifest_path.name}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return build_gui_manifest(capability_id, str(copied_xsd), str(output_dir_path))
