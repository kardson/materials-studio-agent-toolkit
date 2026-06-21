import unittest
from pathlib import Path

from tools.ms_agent_toolkit.templates import render_template


class RenderTemplateTests(unittest.TestCase):
    def test_render_template_applies_defaults_for_optional_parameters(self) -> None:
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
        self.assertIn('Documents->Item("model.xsd")', rendered)
        self.assertIn('Quality => "Coarse"', rendered)


if __name__ == "__main__":
    unittest.main()
