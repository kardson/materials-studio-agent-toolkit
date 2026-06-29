from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolkitConfig:
    run_mat_script_bat: str
    workspace_root: str
    default_project_documents_root: str
    default_timeout_seconds: int
    capability_registry_path: str
    templates_root: str
    knowledge_root: str
    experimental_audit_root: str
    gui_loop_queue_root: str
    gui_loop_poll_seconds: int
    gui_loop_default_wait_seconds: int


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def resolve_config_path(config_dir: Path, base_name: str) -> Path:
    concrete = Path(config_dir) / f"{base_name}.json"
    example = Path(config_dir) / f"{base_name}.example.json"
    if concrete.exists():
        return concrete
    return example


def load_config(bridge_config_path: Path, toolkit_config_path: Path) -> ToolkitConfig:
    bridge = _read_json(Path(bridge_config_path))
    toolkit = _read_json(Path(toolkit_config_path))
    return ToolkitConfig(
        run_mat_script_bat=bridge["runMatScriptBat"],
        workspace_root=bridge["workspaceRoot"],
        default_project_documents_root=bridge["defaultProjectDocumentsRoot"],
        default_timeout_seconds=int(bridge["defaultTimeoutSeconds"]),
        capability_registry_path=toolkit["capabilityRegistryPath"],
        templates_root=toolkit["templatesRoot"],
        knowledge_root=toolkit["KnowledgeRoot"] if "KnowledgeRoot" in toolkit else toolkit["knowledgeRoot"],
        experimental_audit_root=toolkit["experimentalAuditRoot"],
        gui_loop_queue_root=toolkit.get("guiLoopQueueRoot", ""),
        gui_loop_poll_seconds=int(toolkit.get("guiLoopPollSeconds", 2)),
        gui_loop_default_wait_seconds=int(toolkit.get("guiLoopDefaultWaitSeconds", 60)),
    )
