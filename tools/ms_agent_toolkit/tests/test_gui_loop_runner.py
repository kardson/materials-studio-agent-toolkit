import json
import tempfile
import unittest
from pathlib import Path

from tools.ms_agent_toolkit.adapters.gui_loop_runner import enqueue_gui_loop_job, read_gui_loop_job_state


class EnqueueGuiLoopRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "gui_loop"
        self.queue_root = self.root / "queue"
        self.workspace_root = self.root / "workspace"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_enqueue_gui_loop_job_writes_workspace_artifacts_and_pending_script(self) -> None:
        result = enqueue_gui_loop_job(
            queue_root=self.queue_root,
            workspace_root=self.workspace_root,
            job_name="job42.pl",
            rendered_script='print "submitted\\n";',
            manifest={
                "taskId": "job42",
                "taskType": "submit_castep",
                "inputDocument": "model.xsd",
                "outputDocument": "job42.xcd",
                "resultDir": str(self.workspace_root),
                "classification": "production",
                "parameters": {"input_xsd": "model.xsd"},
            },
        )

        self.assertEqual(result["stage"], "task_queued")
        self.assertTrue((self.workspace_root / "job42.pl").exists())
        self.assertTrue((self.queue_root / "pending" / "job42.pl").exists())
        self.assertTrue((self.workspace_root / "task_manifest.json").exists())
        self.assertTrue((self.workspace_root / "run_result.json").exists())

    def test_read_gui_loop_job_state_prefers_status_json(self) -> None:
        logs_dir = self.queue_root / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        (logs_dir / "job42.pl.status.json").write_text(
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

        result = read_gui_loop_job_state(self.queue_root, "job42.pl")

        self.assertEqual(result["state"], "failed")
        self.assertEqual(result["error"], "CASTEP failed")
        self.assertEqual(result["stdoutPath"], "C:/tmp/job42.stdout.txt")


if __name__ == "__main__":
    unittest.main()
