import json
import unittest
from pathlib import Path


class MockBackendContractTests(unittest.TestCase):
    def test_mock_invoke_materialscript_fixture_has_required_keys(self) -> None:
        path = Path(
            r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\tests\mocks\invoke_materialscript_success.json"
        )
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("ok", payload)
        self.assertIn("nativeStdoutPath", payload)
        self.assertIn("nativeLogPath", payload)


if __name__ == "__main__":
    unittest.main()
