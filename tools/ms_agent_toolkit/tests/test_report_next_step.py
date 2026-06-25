import unittest
from unittest.mock import patch

from tools.ms_agent_toolkit.commands.report_next_step import build_report


class BuildReportTests(unittest.TestCase):
    def test_build_report_wraps_result_analysis_into_round_report(self) -> None:
        with patch(
            "tools.ms_agent_toolkit.commands.report_next_step.parse_result_dir",
            return_value={
                "ok": True,
                "stage": "result_parsed",
                "mode": "generic",
                "capabilityId": None,
                "result": {
                    "status": "completed",
                    "task": "GeometryOptimization",
                    "finalEnergyEv": -123.45,
                },
                "analysis": {
                    "summary": "CASTEP GeometryOptimization completed; final energy = -123.45 eV",
                    "status": "completed",
                    "nextStepOptions": [
                        {
                            "optionId": "archive_and_compare",
                            "title": "Archive and compare",
                            "reason": "Result is complete and suitable for publication or cross-run comparison.",
                        }
                    ],
                },
                "evidence": {
                    "castepPath": "C:/tmp/job42.castep",
                    "paramPath": "C:/tmp/job42.param",
                    "summaryPath": None,
                },
                "error": None,
            },
        ):
            report = build_report(module="castep", result_dir="C:/tmp/job42")

        self.assertEqual(report["stage"], "round_report_ready")
        self.assertEqual(report["analysis"]["status"], "completed")
        self.assertEqual(report["archiveRecommendation"]["recommended"], True)
        self.assertEqual(report["nextExecutionPlan"][0]["optionId"], "archive_and_compare")


if __name__ == "__main__":
    unittest.main()
