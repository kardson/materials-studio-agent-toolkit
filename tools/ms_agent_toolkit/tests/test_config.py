import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ms_agent_toolkit.config import load_config, resolve_config_path


class LoadConfigTests(unittest.TestCase):
    def test_resolve_config_path_prefers_concrete_json(self) -> None:
        with patch.object(Path, "exists", side_effect=[True]):
            resolved = resolve_config_path(Path("C:/tmp/config"), "bridge_config")

        self.assertEqual(str(resolved).replace("\\", "/"), "C:/tmp/config/bridge_config.json")

    def test_resolve_config_path_falls_back_to_example_json(self) -> None:
        with patch.object(Path, "exists", side_effect=[False]):
            resolved = resolve_config_path(Path("C:/tmp/config"), "bridge_config")

        self.assertEqual(
            str(resolved).replace("\\", "/"),
            "C:/tmp/config/bridge_config.example.json",
        )

    def test_load_config_merges_bridge_and_toolkit_config(self) -> None:
        bridge = Path("bridge.json")
        toolkit = Path("toolkit.json")
        with patch(
            "tools.ms_agent_toolkit.config._read_json",
            side_effect=[
                {
                    "runMatScriptBat": "C:/MS/RunMatScript.bat",
                    "workspaceRoot": "C:/tmp/ms_bridge_workspace",
                    "defaultProjectDocumentsRoot": "C:/tmp/projects",
                    "defaultTimeoutSeconds": 1800,
                },
                {
                    "capabilityRegistryPath": "C:/tmp/capabilities",
                    "templatesRoot": "C:/tmp/templates",
                    "knowledgeRoot": "C:/tmp/knowledge",
                    "experimentalAuditRoot": "C:/tmp/audit",
                },
            ],
        ) as read_json:
            config = load_config(bridge, toolkit)

        self.assertEqual(config.run_mat_script_bat, "C:/MS/RunMatScript.bat")
        self.assertEqual(config.workspace_root, "C:/tmp/ms_bridge_workspace")
        self.assertEqual(config.default_project_documents_root, "C:/tmp/projects")
        self.assertEqual(config.capability_registry_path, "C:/tmp/capabilities")
        self.assertEqual(config.templates_root, "C:/tmp/templates")
        self.assertEqual(config.knowledge_root, "C:/tmp/knowledge")
        self.assertEqual(config.experimental_audit_root, "C:/tmp/audit")
        self.assertEqual(read_json.call_count, 2)

    def test_load_config_merges_gui_loop_fields(self) -> None:
        bridge = Path("bridge.json")
        toolkit = Path("toolkit.json")
        with patch(
            "tools.ms_agent_toolkit.config._read_json",
            side_effect=[
                {
                    "runMatScriptBat": "C:/MS/RunMatScript.bat",
                    "workspaceRoot": "C:/tmp/ms_bridge_workspace",
                    "defaultProjectDocumentsRoot": "C:/tmp/projects",
                    "defaultTimeoutSeconds": 1800,
                },
                {
                    "capabilityRegistryPath": "C:/tmp/capabilities",
                    "templatesRoot": "C:/tmp/templates",
                    "knowledgeRoot": "C:/tmp/knowledge",
                    "experimentalAuditRoot": "C:/tmp/audit",
                    "guiLoopQueueRoot": "C:/tmp/gui_loop_queue",
                    "guiLoopPollSeconds": 2,
                    "guiLoopDefaultWaitSeconds": 60,
                },
            ],
        ):
            config = load_config(bridge, toolkit)

        self.assertEqual(config.gui_loop_queue_root, "C:/tmp/gui_loop_queue")
        self.assertEqual(config.gui_loop_poll_seconds, 2)
        self.assertEqual(config.gui_loop_default_wait_seconds, 60)


if __name__ == "__main__":
    unittest.main()
