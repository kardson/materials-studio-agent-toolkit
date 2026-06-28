import unittest
import json
from pathlib import Path


class KnowledgeConfigTests(unittest.TestCase):
    def test_knowledge_directory_contains_required_module_subtrees_and_files(self) -> None:
        root = Path(__file__).resolve().parents[1] / "knowledge"
        for module_name in ("materialsscript_core", "castep", "forcite"):
            module_root = root / module_name
            self.assertTrue(module_root.is_dir(), module_name)
            for filename in ("api_summary.md", "parameter_guide.md", "result_semantics.md", "example_index.md"):
                self.assertTrue((module_root / filename).is_file(), f"{module_name}/{filename}")

    def test_example_config_points_to_existing_shipped_knowledge_directory(self) -> None:
        config_path = Path(__file__).resolve().parents[1] / "config" / "toolkit_config.example.json"
        data = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertTrue(Path(data["knowledgeRoot"]).is_dir())


if __name__ == "__main__":
    unittest.main()
