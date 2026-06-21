from __future__ import annotations


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
