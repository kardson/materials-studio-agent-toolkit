import unittest

from tools.ms_agent_toolkit.adapters.gui_submission import build_gui_manifest


class BuildGuiManifestTests(unittest.TestCase):
    def test_manifest_returns_script_generated_stage(self) -> None:
        result = build_gui_manifest(
            capability_id="castep.geometry_optimization",
            input_xsd="input.xsd",
            output_dir="C:/tmp/gui_package",
        )
        self.assertEqual(result["stage"], "script_generated")
        self.assertEqual(result["capabilityId"], "castep.geometry_optimization")


if __name__ == "__main__":
    unittest.main()
