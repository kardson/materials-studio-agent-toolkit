import unittest
from pathlib import Path

from tools.ms_bridge.scripts.read_castep_result import parse_castep_bundle


class ParseCastepBundleTests(unittest.TestCase):
    def test_parse_castep_bundle_reads_final_energy_and_status(self) -> None:
        data_dir = Path(r"C:\Users\kards\Documents\DFT\tools\ms_bridge\tests\data")
        result = parse_castep_bundle(
            castep_file=data_dir / "sample.castep",
            param_file=data_dir / "sample.param",
            summary_file=data_dir / "sample_summary.txt",
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["task"], "SinglePoint")
        self.assertEqual(result["finalEnergyEv"], -138926.3720371)


if __name__ == "__main__":
    unittest.main()
