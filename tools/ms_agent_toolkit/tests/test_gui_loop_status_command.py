import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.ms_agent_toolkit.commands.get_gui_loop_status import get_status


class GetGuiLoopStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "gui_loop_status"
        self.queue_root = self.root / "queue"
        if self.root.exists():
            shutil.rmtree(self.root)
        (self.queue_root / "logs").mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        if self.root.exists():
            shutil.rmtree(self.root)
        self.temp_dir.cleanup()

    def test_get_status_returns_failed_state_from_status_json(self) -> None:
        (self.queue_root / "logs" / "job42.pl.status.json").write_text(
            json.dumps(
                {
                    "script": "job42.pl",
                    "started_at": "Wed Jun 25 10:00:00 2026",
                    "finished_at": "Wed Jun 25 10:05:00 2026",
                    "ok": False,
                    "stdout_file": "C:/tmp/job42.stdout.txt",
                    "error_message": "CASTEP failed",
                }
            ),
            encoding="utf-8",
        )

        status = get_status(self.queue_root, "job42.pl")

        self.assertEqual(status["state"], "failed")
        self.assertEqual(status["error"], "CASTEP failed")


if __name__ == "__main__":
    unittest.main()
