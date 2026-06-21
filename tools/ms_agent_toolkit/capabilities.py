from __future__ import annotations

import json
from pathlib import Path


class CapabilityRegistry:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def get(self, capability_id: str) -> dict:
        path = self.root / f"{capability_id}.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def list_all(self) -> list[dict]:
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self.root.glob("*.json"))
        ]
