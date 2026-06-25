import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ms_agent_toolkit.commands.run_materialscript import build_compliant_request, run_compliant_request


class BuildCompliantRequestTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
