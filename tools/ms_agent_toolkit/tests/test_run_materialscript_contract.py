import unittest

from tools.ms_agent_toolkit.commands.run_materialscript import build_compliant_request


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


if __name__ == "__main__":
    unittest.main()
