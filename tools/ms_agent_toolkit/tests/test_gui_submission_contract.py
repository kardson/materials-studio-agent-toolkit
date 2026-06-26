import json
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ms_agent_toolkit.adapters.gui_submission import build_gui_manifest, write_gui_package
from tools.ms_agent_toolkit.commands.prepare_gui_submission_package import load_gui_package_parameters


class BuildGuiManifestTests(unittest.TestCase):
    def test_load_gui_package_parameters_reads_params_file(self) -> None:
        with patch.object(Path, "read_text", return_value='{"quality":"Fine"}'):
            payload = load_gui_package_parameters(
                params_json=None,
                params_file="C:/tmp/gui_params.json",
            )

        self.assertEqual(payload["quality"], "Fine")

    def test_manifest_returns_script_generated_stage(self) -> None:
        result = build_gui_manifest(
            capability_id="castep.geometry_optimization",
            input_xsd="input.xsd",
            output_dir="C:/tmp/gui_package",
        )
        self.assertEqual(result["stage"], "script_generated")
        self.assertEqual(result["capabilityId"], "castep.geometry_optimization")

    def test_write_gui_package_materializes_expected_files(self) -> None:
        output_dir = Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\tests\_gui_package")
        if output_dir.exists():
            shutil.rmtree(output_dir)
        input_xsd = output_dir.parent / "input.xsd"
        input_xsd.write_text("dummy xsd", encoding="utf-8")
        try:
            result = write_gui_package(
                capability_id="castep.geometry_optimization",
                input_xsd=str(input_xsd),
                output_dir=str(output_dir),
                parameters={"input_xsd": input_xsd.name},
                template_root=Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\templates"),
                capability_root=Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\capabilities"),
            )
            self.assertTrue((output_dir / "job.pl").exists())
            self.assertTrue((output_dir / "task_manifest.json").exists())
            self.assertTrue((output_dir / "README.md").exists())
            self.assertEqual(result["stage"], "script_generated")
        finally:
            if input_xsd.exists():
                input_xsd.unlink()
            if output_dir.exists():
                shutil.rmtree(output_dir)

    def test_write_gui_package_injects_copied_input_name_when_parameters_omit_input_xsd(self) -> None:
        output_dir = Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\tests\_gui_package")
        if output_dir.exists():
            shutil.rmtree(output_dir)
        input_xsd = output_dir.parent / "source_model.xsd"
        input_xsd.write_text("dummy xsd", encoding="utf-8")
        try:
            result = write_gui_package(
                capability_id="castep.geometry_optimization",
                input_xsd=str(input_xsd),
                output_dir=str(output_dir),
                parameters={"quality": "Fine"},
                template_root=Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\templates"),
                capability_root=Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\capabilities"),
            )
            script_text = (output_dir / "job.pl").read_text(encoding="utf-8")
            self.assertIn("source_model.xsd", script_text)
            self.assertEqual(result["stage"], "script_generated")
        finally:
            if input_xsd.exists():
                input_xsd.unlink()
            if output_dir.exists():
                shutil.rmtree(output_dir)


if __name__ == "__main__":
    unittest.main()
