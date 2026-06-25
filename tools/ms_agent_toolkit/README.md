# Materials Studio Agent Toolkit

This toolkit is the thin Python delivery layer for the first Materials Studio agent release in this repo. It does not replace `Materials Studio`, `RunMatScript.bat`, or the existing `tools/ms_bridge` utilities. In M1, it mainly normalizes capability metadata, command payloads, result-reading contracts, and publication-response shapes so human operators and simple agents can call a small, stable interface.

## First-release contents

- Local package metadata in `tools/ms_agent_toolkit/pyproject.toml`
- Four CLI entrypoints defined in that `pyproject.toml`
- Capability registry loader in `tools/ms_agent_toolkit/capabilities.py`
- Capability cards in `tools/ms_agent_toolkit/capabilities/`
- Template renderer in `tools/ms_agent_toolkit/templates.py`
- Shipped template files:
  - `tools/ms_agent_toolkit/templates/standalone/castep_energy.pl.j2`
  - `tools/ms_agent_toolkit/templates/gui/castep_geometry_optimization.pl.j2`
- Thin adapters and command wrappers under `tools/ms_agent_toolkit/adapters/` and `tools/ms_agent_toolkit/commands/`
- Contract tests under `tools/ms_agent_toolkit/tests/`
- Reused backend bridge utilities under `tools/ms_bridge/`

Important current-state note: this release now includes one real standalone execution path, but the toolkit is still only partially operational end to end.

- `run_materialscript` now renders a real `.pl` script, writes execution artifacts, calls the existing PowerShell bridge, and returns a normalized execution result.
- The other commands still focus on packaging metadata, result normalization, and publication response shaping.
- The toolkit still does not provide a complete one-shot orchestrator for a full Materials Studio workflow.

## Python and install requirements

The package metadata lives at `tools/ms_agent_toolkit/pyproject.toml`. It currently declares:

- Python: `>=3.12`
- Build backend: `setuptools>=68`
- Runtime dependencies:
  - `pydantic>=2.0`
  - `jinja2>=3.1`

It also declares these console-script names:

- `run_materialscript`
- `prepare_gui_submission_package`
- `read_module_result`
- `publish_to_project_documents`

Practical note: this repo currently ships the local `pyproject.toml`, command modules, and package code, but not a separate polished release/install workflow beyond that. Treat the `pyproject.toml` as the source of truth for Python version, dependencies, and entrypoint names.

## Configuration on a new machine

Two JSON example files matter:

- Bridge config: `tools/ms_bridge/config/bridge_config.example.json`
- Toolkit config: `tools/ms_agent_toolkit/config/toolkit_config.example.json`

`tools/ms_agent_toolkit/config.py` merges values from both files into one runtime config object.

Fields that must be reviewed on a new machine:

- In `bridge_config.example.json`:
  - `materialsStudioInstallRoot`
  - `runMatScriptBat`
  - `workspaceRoot`
  - `defaultProjectDocumentsRoot`
  - `defaultTimeoutSeconds`
  - `productionResultMode`
- In `toolkit_config.example.json`:
  - `capabilityRegistryPath`
  - `templatesRoot`
  - `knowledgeRoot`
  - `experimentalAuditRoot`

### `RunMatScript.bat`

`RunMatScript.bat` is not included inside this repo. It comes from the local BIOVIA Materials Studio installation and is the main machine-specific setting to fix first.

Update `runMatScriptBat` in `tools/ms_bridge/config/bridge_config.example.json` so it points to the real local batch file, for example:

```json
"runMatScriptBat": "C:\\Program Files (x86)\\BIOVIA\\Materials Studio 24.1\\etc\\Scripting\\bin\\RunMatScript.bat"
```

Also review `materialsStudioInstallRoot` to match the installed version on that machine. If those paths are wrong, the PowerShell bridge at `tools/ms_bridge/scripts/invoke_materialscript.ps1` will fail before any MaterialsScript can run.

One more current-state caveat: `toolkit_config.example.json` includes `knowledgeRoot`, but this repo does not currently ship a `tools/ms_agent_toolkit/knowledge/` directory. Set that path intentionally if you add one later, or keep in mind that knowledge-pack content is not part of this delivery.

## Command entrypoints

These names come directly from `tools/ms_agent_toolkit/pyproject.toml`.

### `run_materialscript`

Purpose: execute a compliant standalone capability through the existing `ms_bridge` path and return a normalized execution result.

Example:

```powershell
run_materialscript --capability castep.energy --params-json "{\"input_xsd\":\"C:/work/model.xsd\",\"quality\":\"Fine\"}"
```

Current behavior in the current branch:

- Reads a capability card from `tools/ms_agent_toolkit/capabilities/`
- Verifies required and allowed parameters
- Resolves the correct template
- Renders a real `.pl` script
- Writes `task_manifest.json`
- Calls `tools/ms_bridge/scripts/invoke_materialscript.ps1`
- Writes `run_result.json`
- Returns normalized execution output with evidence paths

### `prepare_gui_submission_package`

Purpose: print a JSON manifest describing the expected GUI submission package artifact paths.

Example:

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package
```

Current behavior in M1:

- Returns `stage: "script_generated"`
- Returns expected paths for `task_manifest.json`, `job.pl`, and `README.md`
- Does not itself write those files yet

### `read_module_result`

Purpose: parse an existing result directory into a normalized JSON result.

Example:

```powershell
read_module_result --module castep --result-dir C:/work/job42
```

Current behavior in M1:

- Only `castep` is supported
- Expects to find one `*.castep` file and one `*.param` file
- Optionally includes a `*summary*.txt`
- Returns `stage: "result_parsed"` with evidence paths and parsed result content

### `publish_to_project_documents`

Purpose: print a normalized publication response for files that are meant to be considered published into project documents.

Example:

```powershell
publish_to_project_documents --source-path C:/work/job42/output.xcd --source-path C:/work/job42/report.txt --project-documents-root C:/Projects/MyProject/Documents
```

Current behavior in M1:

- Returns `stage: "gui_publication_completed"`
- Returns `publishedPaths` and the expected `task_manifest.json` path
- Does not itself copy files into the project tree

## Capability cards and templates

Capability cards live in:

- `tools/ms_agent_toolkit/capabilities/`

Current cards in this delivery:

- `castep.energy.json`
- `castep.geometry_optimization.json`
- `forcite.geometry_optimization.json`

Current-state detail: `forcite.geometry_optimization.json` is only a reserved placeholder with `status: "reserved"` and no supported execution modes yet.

Templates live in:

- `tools/ms_agent_toolkit/templates/standalone/`
- `tools/ms_agent_toolkit/templates/gui/`

Shipped template files:

- `tools/ms_agent_toolkit/templates/standalone/castep_energy.pl.j2`
- `tools/ms_agent_toolkit/templates/gui/castep_geometry_optimization.pl.j2`

## How skill-capable agents should use `SKILL.md`

The generic skill guide for this toolkit is:

- `skills/materials-studio-agent-toolkit/SKILL.md`

It is meant as a lightweight operating guide, not as a hidden source of extra implementation. Skill-capable agents should use it to:

- Prefer a capability card first
- Stay in compliant mode when a shipped capability exists
- Treat result `stage` values as execution-state signals
- Avoid treating the toolkit as a scientific decision engine

In practice, the skill file should be read together with:

- The capability card for the requested task
- The command wrapper being called
- The underlying `tools/ms_bridge/` scripts when actual execution behavior matters

Non-skill-capable agents can ignore `SKILL.md` and use this README plus the capability JSON files directly.

## Not included yet

This first version does not yet include:

- A direct end-to-end execution command that runs the generated backend command for you
- A complete GUI package writer that materializes `job.pl`, `task_manifest.json`, and README files on disk
- A real publication copier that moves files into the Materials Studio project tree
- Result readers beyond `castep`
- An implemented `forcite.geometry_optimization` flow
- A shipped `tools/ms_agent_toolkit/knowledge/` directory, despite the reserved `knowledgeRoot` config field
- Experimental-mode command handling in the delivered CLI wrappers
- A full MCP server package under this toolkit directory

For actual backend execution and low-level bridge behavior, continue to inspect and reuse `tools/ms_bridge/`.
