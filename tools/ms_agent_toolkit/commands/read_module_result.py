from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.adapters.result_readers.castep import parse_result_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--result-dir", required=True)
    args = parser.parse_args()
    if args.module != "castep":
        raise SystemExit("Only castep is supported in the first release.")
    print(json.dumps(parse_result_dir(Path(args.result_dir)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
