import unittest

from tools.ms_agent_toolkit.commands.run_materialscript import build_compliant_request


class BuildCompliantRequestTests(unittest.TestCase):
    def test_build_request_reads_params_json(self) -> None:
        request = build_compliant_request(
            capability_id="castep.energy",
            params_json='{"input_xsd":"model.xsd","quality":"Fine"}',
        )
        self.assertEqual(request["capabilityId"], "castep.energy")
        self.assertEqual(request["parameters"]["input_xsd"], "model.xsd")
        self.assertEqual(request["parameters"]["quality"], "Fine")


if __name__ == "__main__":
    unittest.main()
