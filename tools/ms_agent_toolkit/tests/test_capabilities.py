import unittest
from pathlib import Path

from tools.ms_agent_toolkit.capabilities import CapabilityRegistry


class CapabilityRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = CapabilityRegistry(Path(__file__).resolve().parent.parent / "capabilities")

    def test_registry_loads_castep_energy_card(self) -> None:
        card = self.registry.get("castep.energy")
        self.assertEqual(card["capability_id"], "castep.energy")
        self.assertEqual(card["module"], "CASTEP")
        self.assertEqual(card["result_reader"], "castep")
        self.assertEqual(card["supported_execution_modes"], ["compliant"])
        self.assertIn("cutoff_energy", card["allowed_parameters"])
        self.assertIn("kpoint_grid", card["allowed_parameters"])
        self.assertEqual(
            card["official_example_refs"],
            ["tools/ms_bridge/materials/templates/submit_castep_template.pl"],
        )

    def test_registry_loads_castep_geometry_optimization_card(self) -> None:
        card = self.registry.get("castep.geometry_optimization")
        self.assertEqual(card["capability_id"], "castep.geometry_optimization")
        self.assertEqual(card["module"], "CASTEP")
        self.assertEqual(card["task"], "GeometryOptimization")
        self.assertEqual(card["result_reader"], "castep")
        self.assertEqual(
            card["official_example_refs"],
            ["tools/gateway_agent_bridge/perl/gui_castep_go_s1_v2_5b.pl"],
        )

    def test_registry_lists_all_capability_ids(self) -> None:
        cards = self.registry.list_all()
        capability_ids = {card["capability_id"] for card in cards}
        self.assertEqual(
            capability_ids,
            {
                "castep.energy",
                "castep.geometry_optimization",
                "forcite.geometry_optimization",
            },
        )

    def test_registry_rejects_capability_path_escape_attempt(self) -> None:
        with self.assertRaises(ValueError):
            self.registry.get("..\\outside")

    def test_registry_reports_definition_pending_forcite_geometry_optimization(self) -> None:
        card = self.registry.get("forcite.geometry_optimization")
        self.assertEqual(card["module"], "Forcite")
        self.assertEqual(card["task"], "GeometryOptimization")
        self.assertEqual(card["result_reader"], "forcite")
        self.assertEqual(
            card["official_doc_refs"],
            [
                "C:\\Program Files (x86)\\BIOVIA\\Materials Studio 24.1\\share\\doc\\content\\scripting\\forcitescripting\\apiforcite.htm",
                "C:\\Program Files (x86)\\BIOVIA\\Materials Studio 24.1\\share\\doc\\content\\scripting\\forcitescripting\\apiforcitegeometryoptimization.htm",
            ],
        )
        self.assertEqual(
            card["official_example_refs"],
            [
                "C:\\Program Files (x86)\\BIOVIA\\Materials Studio 24.1\\share\\Examples\\Projects\\Forcite\\SolvationFreeEnergy.stp",
            ],
        )
        self.assertEqual(card["supported_execution_modes"], [])
        self.assertEqual(
            card["notes"],
            "Definition-complete only; no template is shipped, execution remains pending, and execution is not approved in this phase.",
        )

    def test_registry_loads_definition_complete_forcite_geometry_optimization_card(self) -> None:
        card = self.registry.get("forcite.geometry_optimization")
        for field in (
            "capability_id",
            "module",
            "task",
            "official_api_signature",
            "official_doc_refs",
            "official_example_refs",
            "template_id",
            "allowed_parameters",
            "required_inputs",
            "result_reader",
            "supported_execution_modes",
            "notes",
        ):
            self.assertIn(field, card)


if __name__ == "__main__":
    unittest.main()
