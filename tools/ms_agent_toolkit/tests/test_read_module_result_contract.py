import unittest
from pathlib import Path

from tools.ms_agent_toolkit.adapters.result_readers.castep import parse_result_dir


class ParseResultDirTests(unittest.TestCase):
    def test_parse_result_dir_returns_completed_status(self) -> None:
        result = parse_result_dir(
            result_dir=Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_bridge\tests\data")
        )
        self.assertEqual(result["stage"], "result_parsed")
        self.assertEqual(result["mode"], "generic")
        self.assertEqual(result["result"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
