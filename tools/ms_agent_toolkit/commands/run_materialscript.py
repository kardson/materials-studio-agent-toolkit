from __future__ import annotations

import argparse
import json


def build_compliant_request(capability_id: str, params_json: str) -> dict:
    return {
        "capabilityId": capability_id,
        "parameters": json.loads(params_json),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capability", required=True)
    parser.add_argument("--params-json", required=True)
    args = parser.parse_args()
    print(json.dumps(build_compliant_request(args.capability, args.params_json), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
