import unittest

from tools.ms_bridge.scripts.publish_to_project_documents import build_publish_summary


class BuildPublishSummaryTests(unittest.TestCase):
    def test_build_publish_summary_has_core_fields(self) -> None:
        response = {
            "ok": True,
            "nativeStdout": "published_to_project_documents_ok\nC:\\target\\file.xsd\n",
            "nativeLogPath": "C:\\logs\\publish.htm",
        }
        summary = build_publish_summary(
            manifest_path="C:/tmp/task_manifest.json",
            run_result_path="C:/tmp/run_result.json",
            bridge_response=response,
        )
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["manifestPath"], "C:/tmp/task_manifest.json")
        self.assertEqual(summary["runResultPath"], "C:/tmp/run_result.json")
        self.assertEqual(summary["publishedPath"], "C:\\target\\file.xsd")
        self.assertEqual(summary["nativeLogPath"], "C:\\logs\\publish.htm")


if __name__ == "__main__":
    unittest.main()
