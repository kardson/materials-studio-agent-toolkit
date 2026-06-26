import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ms_agent_toolkit.commands.run_materialscript import (
    _resolve_config_path,
    build_compliant_request,
    run_compliant_request,
)


class BuildCompliantRequestTests(unittest.TestCase):
    def test_resolve_config_path_prefers_concrete_json_over_example(self) -> None:
        with patch.object(Path, "exists", side_effect=[True]):
            resolved = _resolve_config_path(Path("C:/tmp/config"), "bridge_config")

        self.assertEqual(str(resolved).replace("\\", "/"), "C:/tmp/config/bridge_config.json")

    def test_build_request_reads_params_json_and_wires_backend_contract(self) -> None:
        request = build_compliant_request(
            capability_id="castep.energy",
            params_json='{"input_xsd":"model.xsd","quality":"Fine"}',
        )
        self.assertEqual(request["mode"], "compliant")
        self.assertEqual(request["capabilityId"], "castep.energy")
        self.assertEqual(request["module"], "CASTEP")
        self.assertEqual(request["task"], "Energy")
        self.assertEqual(request["parameters"]["input_xsd"], "model.xsd")
        self.assertEqual(request["parameters"]["quality"], "Fine")
        self.assertEqual(request["backend"]["manifest"]["taskType"], "submit_castep")
        self.assertEqual(request["backend"]["manifest"]["inputDocument"], "model.xsd")
        self.assertEqual(
            request["backend"]["manifest"]["parameters"]["quality"],
            "Fine",
        )
        self.assertIn("invoke_materialscript.ps1", request["backend"]["command"])
        self.assertIn("-ScriptArguments @('model.xsd')", request["backend"]["command"])

    def test_run_compliant_request_executes_and_writes_artifacts(self) -> None:
        with patch(
            "tools.ms_agent_toolkit.commands.run_materialscript.load_config"
        ) as load_config_mock, patch(
            "tools.ms_agent_toolkit.commands.run_materialscript.render_template",
            return_value="rendered script",
        ), patch(
            "tools.ms_agent_toolkit.commands.run_materialscript.execute_backend_contract",
            return_value={
                "manifestPath": "C:/tmp/task_manifest.json",
                "runResultPath": "C:/tmp/run_result.json",
                "bridgeResponse": {
                    "ok": True,
                    "nativeStdout": "submitted\n",
                    "nativeStdoutPath": "C:/tmp/job.pl.out",
                    "nativeLogPath": "C:/tmp/jobMatStudioLog.htm",
                },
                "runResult": {"ok": True, "error": None},
            },
        ), patch.object(Path, "write_text", return_value=None):
            load_config_mock.return_value = type(
                "Cfg",
                (),
                {"run_mat_script_bat": "C:/MS/RunMatScript.bat"},
            )()
            result = run_compliant_request(
                capability_id="castep.energy",
                params_json=json.dumps({"input_xsd": "model.xsd", "quality": "Fine"}),
            )

        self.assertTrue(result["ok"])
        self.assertEqual(result["stage"], "task_submitted")
        self.assertEqual(result["mode"], "compliant")
        self.assertEqual(result["capabilityId"], "castep.energy")
        self.assertEqual(result["evidence"]["manifestPath"], "C:/tmp/task_manifest.json")
        self.assertEqual(result["evidence"]["runResultPath"], "C:/tmp/run_result.json")
        self.assertEqual(result["evidence"]["nativeStdoutPath"], "C:/tmp/job.pl.out")

    def test_run_compliant_request_enqueues_gui_loop_job(self) -> None:
        with patch(
            "tools.ms_agent_toolkit.commands.run_materialscript.load_config"
        ) as load_config_mock, patch(
            "tools.ms_agent_toolkit.commands.run_materialscript.render_template",
            return_value="rendered script",
        ), patch(
            "tools.ms_agent_toolkit.commands.run_materialscript.enqueue_gui_loop_job",
            return_value={
                "stage": "task_queued",
                "scriptPath": "C:/tmp/gui_loop_queue/pending/job42.pl",
                "manifestPath": "C:/tmp/workspace/task_manifest.json",
                "runResultPath": "C:/tmp/workspace/run_result.json",
            },
        ), patch.object(Path, "write_text", return_value=None):
            load_config_mock.return_value = type(
                "Cfg",
                (),
                {
                    "run_mat_script_bat": "C:/MS/RunMatScript.bat",
                    "gui_loop_queue_root": "C:/tmp/gui_loop_queue",
                },
            )()
            result = run_compliant_request(
                capability_id="castep.geometry_optimization",
                params_json=json.dumps({"input_xsd": "model.xsd", "quality": "Fine"}),
                backend="gui_loop",
            )

        self.assertTrue(result["ok"])
        self.assertEqual(result["stage"], "task_queued")
        self.assertEqual(result["backend"], "gui_loop")
        self.assertEqual(result["capabilityId"], "castep.geometry_optimization")
        self.assertEqual(
            result["evidence"]["queuedScriptPath"],
            "C:/tmp/gui_loop_queue/pending/job42.pl",
        )

    def test_build_gui_loop_request_uses_gui_document_name_in_template_parameters(self) -> None:
        request = build_compliant_request(
            capability_id="castep.geometry_optimization",
            params_json='{"input_xsd":"C:/work/model.xsd","quality":"Fine"}',
            backend="gui_loop",
        )

        self.assertEqual(request["parameters"]["input_xsd"], "model.xsd")
        self.assertEqual(request["backend"]["manifest"]["inputDocument"], "C:/work/model.xsd")


if __name__ == "__main__":
    unittest.main()
