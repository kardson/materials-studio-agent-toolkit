from __future__ import annotations

import argparse
import json

from tools.ms_agent_toolkit.adapters.publication import build_publication_response


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-path", action="append", required=True)
    parser.add_argument("--project-documents-root", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            build_publication_response(
                published_paths=args.source_path,
                manifest_path=f"{args.project_documents_root}/task_manifest.json",
            ),
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
