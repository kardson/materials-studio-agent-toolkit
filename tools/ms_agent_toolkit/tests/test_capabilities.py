import unittest
from pathlib import Path

from tools.ms_agent_toolkit.capabilities import CapabilityRegistry


class CapabilityRegistryTests(unittest.TestCase):
    def test_registry_loads_castep_energy_card(self) -> None:
        registry = CapabilityRegistry(
            Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\capabilities")
        )
        card = registry.get("castep.energy")
        self.assertEqual(card["capability_id"], "castep.energy")
        self.assertEqual(card["module"], "CASTEP")
        self.assertEqual(card["result_reader"], "castep")
        self.assertEqual(card["supported_execution_modes"], ["compliant"])

    def test_registry_reports_reserved_capability(self) -> None:
        registry = CapabilityRegistry(
            Path(r"C:\Users\kards\Documents\DFT_materials_studio_mcp_m1\tools\ms_agent_toolkit\capabilities")
        )
        card = registry.get("forcite.geometry_optimization")
        self.assertEqual(card["status"], "reserved")


if __name__ == "__main__":
    unittest.main()
