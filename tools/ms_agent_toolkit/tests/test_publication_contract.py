import shutil
import unittest
from pathlib import Path

from tools.ms_agent_toolkit.adapters.publication import build_publication_response, publish_files


class BuildPublicationResponseTests(unittest.TestCase):
    def test_publication_response_uses_generic_mode(self) -> None:
        result = build_publication_response(
            published_paths=["C:/target/file.xsd"],
            manifest_path="C:/tmp/task_manifest.json",
            run_result_path="C:/tmp/run_result.json",
        )
        self.assertEqual(result["mode"], "generic")
        self.assertEqual(result["stage"], "gui_publication_completed")

    def test_publish_files_copies_sources_and_writes_manifest(self) -> None:
        root = Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\tests\_publish")
        source_dir = root / "source"
        target_dir = root / "target"
        if root.exists():
            shutil.rmtree(root)
        source_dir.mkdir(parents=True)
        target_dir.mkdir(parents=True)
        source_file = source_dir / "result.xsd"
        source_file.write_text("payload", encoding="utf-8")
        try:
            result = publish_files(
                source_paths=[str(source_file)],
                project_documents_root=str(target_dir),
            )
            self.assertEqual(result["mode"], "generic")
            self.assertEqual(result["stage"], "gui_publication_completed")
            self.assertTrue((target_dir / "result.xsd").exists())
            self.assertTrue((target_dir / "task_manifest.json").exists())
        finally:
            if root.exists():
                shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()
