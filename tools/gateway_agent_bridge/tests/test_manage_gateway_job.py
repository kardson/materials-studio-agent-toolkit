import unittest

from tools.gateway_agent_bridge.scripts.manage_gateway_job import parse_create_job_stdout


class ParseCreateJobStdoutTests(unittest.TestCase):
    def test_parse_create_job_stdout_extracts_job_id(self) -> None:
        stdout = "Gw-status-code: 600\nGw-status-text: OK\nContent-Type: text/plain; charset=ISO-8859-1\n\nB6S3G\n"
        parsed = parse_create_job_stdout(stdout)
        self.assertEqual(parsed["jobId"], "B6S3G")


if __name__ == "__main__":
    unittest.main()
