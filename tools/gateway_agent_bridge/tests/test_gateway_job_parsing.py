import unittest

from tools.gateway_agent_bridge.scripts.query_gateway_job import parse_gateway_status


class ParseGatewayStatusTests(unittest.TestCase):
    def test_parse_gateway_status_extracts_core_fields(self) -> None:
        raw = {
            "jobId": "abc123",
            "status": "running",
            "progress": "42",
            "resultsFolder": "/Project/Results/Job1",
        }
        parsed = parse_gateway_status(raw)
        self.assertEqual(parsed["jobId"], "abc123")
        self.assertEqual(parsed["status"], "running")
        self.assertEqual(parsed["progress"], "42")
        self.assertEqual(parsed["resultsFolder"], "/Project/Results/Job1")
