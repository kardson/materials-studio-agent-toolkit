from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.config import load_config, resolve_config_path


def path_exists(path: Path) -> bool:
    return Path(path).exists()


def build_doctor_report() -> dict:
    repo_root = Path(__file__).resolve().parents[3]
    toolkit_root = Path(__file__).resolve().parents[1]
    bridge_config_path = resolve_config_path(repo_root / "tools" / "ms_bridge" / "config", "bridge_config")
    toolkit_config_path = resolve_config_path(toolkit_root / "config", "toolkit_config")
    config = load_config(bridge_config_path, toolkit_config_path)

    runmatscript = Path(config.run_mat_script_bat)
    gui_loop_queue = Path(config.gui_loop_queue_root)

    return {
        "ok": True,
        "stage": "doctor_report_ready",
        "mode": "generic",
        "isMcpServer": False,
        "configPaths": {
            "bridge": str(bridge_config_path),
            "toolkit": str(toolkit_config_path),
        },
        "checks": {
            "runMatScriptBat": {
                "path": str(runmatscript),
                "ok": path_exists(runmatscript),
            },
            "guiLoopQueueRoot": {
                "path": str(gui_loop_queue),
                "ok": path_exists(gui_loop_queue),
            },
        },
        "notes": [
            "This project is a CLI toolkit, not an MCP server.",
            "GUI loop execution requires a separately running Materials Studio GUI-resident loop.",
        ],
        "error": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(build_doctor_report(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
