from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def resolve_template_path(template_root: Path, template_id: str) -> Path:
    mapping = {
        "castep.energy.basic": Path("standalone") / "castep_energy.pl.j2",
        "castep.geometry_optimization.gui": Path("gui") / "castep_geometry_optimization.pl.j2",
    }
    try:
        relative = mapping[template_id]
    except KeyError as exc:
        raise ValueError(f"Unknown template id: {template_id}") from exc
    return Path(template_root) / relative


def render_template(template_path: Path, parameters: dict) -> str:
    template_path = Path(template_path)
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**parameters)
