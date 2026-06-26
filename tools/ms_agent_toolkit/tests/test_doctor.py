import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ms_agent_toolkit.commands.doctor import build_doctor_report


class DoctorReportTests(unittest.TestCase):
    def test_build_doctor_report_reports_config_and_runtime_preconditions(self) -> None:
        fake_config = type(
            "Cfg",
            (),
            {
                "run_mat_script_bat": "C:/MS/RunMatScript.bat",
                "gui_loop_queue_root": "C:/tmp/gui_loop_queue",
            },
        )()

        with patch(
            "tools.ms_agent_toolkit.commands.doctor.resolve_config_path",
            side_effect=[
                Path("C:/tmp/bridge_config.json"),
                Path("C:/tmp/toolkit_config.json"),
            ],
        ), patch(
            "tools.ms_agent_toolkit.commands.doctor.load_config",
            return_value=fake_config,
        ), patch(
            "tools.ms_agent_toolkit.commands.doctor.path_exists",
            side_effect=lambda path: str(path).replace("\\", "/")
            in {
                "C:/tmp/bridge_config.json",
                "C:/tmp/toolkit_config.json",
                "C:/MS/RunMatScript.bat",
                "C:/tmp/gui_loop_queue",
            },
        ):
            report = build_doctor_report()

        self.assertEqual(report["stage"], "doctor_report_ready")
        self.assertFalse(report["isMcpServer"])
        self.assertTrue(report["checks"]["runMatScriptBat"]["ok"])
        self.assertTrue(report["checks"]["guiLoopQueueRoot"]["ok"])


if __name__ == "__main__":
    unittest.main()
