from __future__ import annotations

import json
from pathlib import Path


def load_params_payload(*, params_json: str | None, params_file: str | None) -> dict:
    if params_file:
        return json.loads(Path(params_file).read_text(encoding="utf-8"))
    if params_json is None:
        return {}
    return json.loads(params_json)
