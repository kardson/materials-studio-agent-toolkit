from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.ms_agent_toolkit.adapters.gui_submission import write_gui_package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capability", required=True)
    parser.add_argument("--input-xsd", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--params-json", default="{}")
    args = parser.parse_args()
    print(
        json.dumps(
            write_gui_package(
                capability_id=args.capability,
                input_xsd=args.input_xsd,
                output_dir=args.output_dir,
                parameters=json.loads(args.params_json),
                template_root=Path(__file__).resolve().parents[1] / "templates",
                capability_root=Path(__file__).resolve().parents[1] / "capabilities",
            ),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
