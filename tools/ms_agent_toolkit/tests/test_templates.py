import unittest
from pathlib import Path

from tools.ms_agent_toolkit.templates import render_template


class RenderTemplateTests(unittest.TestCase):
    def test_render_template_imports_input_and_applies_defaults(self) -> None:
        template_path = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "standalone"
            / "castep_energy.pl.j2"
        )
        rendered = render_template(
            template_path=template_path,
            parameters={"input_xsd": "model.xsd"},
        )
        self.assertIn('Documents->Import("model.xsd")', rendered)
        self.assertIn('Quality => "Coarse"', rendered)


if __name__ == "__main__":
    unittest.main()
