import unittest

from tools.ms_bridge.scripts.write_task_manifest import build_manifest


class BuildManifestTests(unittest.TestCase):
    def test_build_manifest_has_required_fields(self) -> None:
        manifest = build_manifest(
            task_id="task-001",
            task_type="submit_castep",
            input_document="S1_v2_GaAs100_6L_2x2_singleO_init.xsd",
            output_document="CASTEP_S1_V2_5B_singleO_opt",
            result_dir="C:/tmp/result",
            classification="production",
            parameters={"Quality": "Coarse"},
        )
        self.assertEqual(manifest["taskId"], "task-001")
        self.assertEqual(manifest["taskType"], "submit_castep")
        self.assertEqual(manifest["classification"], "production")
        self.assertIn("createdAt", manifest)
        self.assertEqual(manifest["parameters"]["Quality"], "Coarse")


if __name__ == "__main__":
    unittest.main()
