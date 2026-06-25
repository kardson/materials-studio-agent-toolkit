from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.adapters.gui_loop_runner import read_gui_loop_job_state


def get_status(queue_root: Path, job_name: str) -> dict:
    return read_gui_loop_job_state(Path(queue_root), job_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue-root", required=True)
    parser.add_argument("--job-name", required=True)
    args = parser.parse_args()
    print(json.dumps(get_status(Path(args.queue_root), args.job_name), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
