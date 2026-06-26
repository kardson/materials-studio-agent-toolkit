import tomllib
import unittest
from pathlib import Path


class PyprojectMetadataTests(unittest.TestCase):
    def test_pyproject_declares_repo_root_package_dir_for_editable_install(self) -> None:
        pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
        data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

        self.assertEqual(
            data["tool"]["setuptools"]["package-dir"][""],
            "../..",
        )


if __name__ == "__main__":
    unittest.main()
