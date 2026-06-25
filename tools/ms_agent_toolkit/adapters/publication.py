from __future__ import annotations

import shutil
from pathlib import Path


def build_publication_response(
    published_paths: list[str],
    manifest_path: str,
    run_result_path: str | None = None,
) -> dict:
    evidence = {
        "publishedPaths": published_paths,
        "manifestPath": manifest_path,
    }
    if run_result_path is not None:
        evidence["runResultPath"] = run_result_path
    return {
        "ok": True,
        "stage": "gui_publication_completed",
        "mode": "generic",
        "capabilityId": None,
        "error": None,
        "evidence": evidence,
    }


def publish_files(
    *,
    source_paths: list[str],
    project_documents_root: str,
) -> dict:
    root = Path(project_documents_root)
    root.mkdir(parents=True, exist_ok=True)
    published_paths: list[str] = []
    for source in source_paths:
        src = Path(source)
        dest = root / src.name
        shutil.copy2(src, dest)
        published_paths.append(str(dest))
    manifest_path = root / "task_manifest.json"
    manifest_path.write_text(
        "{\n"
        f'  "publishedCount": {len(published_paths)},\n'
        f'  "targetRoot": "{str(root).replace("\\", "\\\\")}"\n'
        "}\n",
        encoding="utf-8",
    )
    return build_publication_response(
        published_paths=published_paths,
        manifest_path=str(manifest_path),
    )
