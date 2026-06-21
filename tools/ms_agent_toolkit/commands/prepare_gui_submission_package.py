from __future__ import annotations

import argparse
import json

from tools.ms_agent_toolkit.adapters.gui_submission import build_gui_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capability", required=True)
    parser.add_argument("--input-xsd", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            build_gui_manifest(args.capability, args.input_xsd, args.output_dir),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
