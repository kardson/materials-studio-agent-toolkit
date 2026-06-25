import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ms_agent_toolkit.adapters.result_readers.castep import parse_result_dir


class ParseResultDirTests(unittest.TestCase):
    def test_parse_result_dir_discovers_expected_files_and_returns_completed_status(self) -> None:
        result_dir = Path(
            r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_bridge\tests\data"
        )

        def fake_glob(self: Path, pattern: str) -> list[Path]:
            if pattern == "*.castep":
                return [self / "job42.castep"]
            if pattern == "*.param":
                return [self / "job42.param"]
            if pattern == "*summary*.txt":
                return [self / "job42_summary.txt"]
            return []

        with patch("pathlib.Path.glob", new=fake_glob), patch(
            "tools.ms_agent_toolkit.adapters.result_readers.castep.parse_castep_bundle",
            return_value={"status": "completed"},
        ):
            result = parse_result_dir(
                result_dir=result_dir
            )

        self.assertEqual(result["stage"], "result_parsed")
        self.assertEqual(result["mode"], "generic")
        self.assertEqual(result["result"]["status"], "completed")
        self.assertTrue(result["evidence"]["castepPath"].endswith("job42.castep"))
        self.assertTrue(result["evidence"]["paramPath"].endswith("job42.param"))
        self.assertTrue(result["evidence"]["summaryPath"].endswith("job42_summary.txt"))
        self.assertIn("analysis", result)
        self.assertIn("summary", result["analysis"])
        self.assertIn("nextStepOptions", result["analysis"])
        self.assertEqual(result["analysis"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
