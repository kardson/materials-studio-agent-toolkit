import unittest

from tools.ms_agent_toolkit.adapters.publication import build_publication_response


class BuildPublicationResponseTests(unittest.TestCase):
    def test_publication_response_uses_generic_mode(self) -> None:
        result = build_publication_response(
            published_paths=["C:/target/file.xsd"],
            manifest_path="C:/tmp/task_manifest.json",
            run_result_path="C:/tmp/run_result.json",
        )
        self.assertEqual(result["mode"], "generic")
        self.assertEqual(result["stage"], "gui_publication_completed")


if __name__ == "__main__":
    unittest.main()
