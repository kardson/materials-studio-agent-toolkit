import json
import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from tools.ms_agent_toolkit.config import load_config


class LoadConfigTests(unittest.TestCase):
    def test_load_config_merges_bridge_and_toolkit_config(self) -> None:
        tmp_root = Path.home() / ".cache" / "ms_agent_toolkit_tests"
        tmp_root.mkdir(parents=True, exist_ok=True)
        tmp_path = tmp_root / f"_tmp_{uuid4().hex}"
        tmp_path.mkdir()
        try:
            bridge = tmp_path / "bridge.json"
            toolkit = tmp_path / "toolkit.json"
            bridge.write_text(
                json.dumps(
                    {
                        "runMatScriptBat": "C:/MS/RunMatScript.bat",
                        "workspaceRoot": "C:/tmp/ms_bridge_workspace",
                        "defaultProjectDocumentsRoot": "C:/tmp/projects",
                        "defaultTimeoutSeconds": 1800,
                    }
                ),
                encoding="utf-8",
            )
            toolkit.write_text(
                json.dumps(
                    {
                        "capabilityRegistryPath": "C:/tmp/capabilities",
                        "templatesRoot": "C:/tmp/templates",
                        "knowledgeRoot": "C:/tmp/knowledge",
                        "experimentalAuditRoot": "C:/tmp/audit",
                    }
                ),
                encoding="utf-8",
            )

            config = load_config(bridge, toolkit)

            self.assertEqual(config.run_mat_script_bat, "C:/MS/RunMatScript.bat")
            self.assertEqual(config.workspace_root, "C:/tmp/ms_bridge_workspace")
            self.assertEqual(config.default_project_documents_root, "C:/tmp/projects")
            self.assertEqual(config.capability_registry_path, "C:/tmp/capabilities")
            self.assertEqual(config.templates_root, "C:/tmp/templates")
            self.assertEqual(config.knowledge_root, "C:/tmp/knowledge")
            self.assertEqual(config.experimental_audit_root, "C:/tmp/audit")
        finally:
            shutil.rmtree(tmp_path)


if __name__ == "__main__":
    unittest.main()
