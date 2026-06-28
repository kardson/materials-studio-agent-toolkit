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

Important current-state note: this release now includes one real standalone execution path, one real GUI-loop queue execution path, one real GUI package writer, one real local publication step, and one first-pass result-analysis layer.

- `run_materialscript` now renders a real `.pl` script, writes execution artifacts, calls the existing PowerShell bridge, and returns a normalized execution result.
- `run_materialscript --backend gui_loop` now renders a real `.pl` script, writes isolated workspace artifacts, and enqueues the script into the isolated GUI-loop queue for a Materials Studio GUI-resident runner.
- `prepare_gui_submission_package` now writes a real package skeleton to disk, including a copied input `.xsd`, a rendered `.pl`, `task_manifest.json`, and `README.md`.
- `read_module_result` now returns both parsed raw results and a lightweight analysis block with a summary and candidate next-step options.
- `publish_to_project_documents` now performs a real local file publication into the target documents directory and writes a publication manifest.
- The toolkit still does not provide a single fully automatic orchestrator that starts the Materials Studio GUI loop itself.

## Python and install requirements

The package metadata lives at `tools/ms_agent_toolkit/pyproject.toml`. It currently declares:

- Python: `>=3.12`
- Build backend: `setuptools>=68`
- Runtime dependencies:
  - `pydantic>=2.0`
  - `jinja2>=3.1`

It also declares these console-script names:

- `ms_agent_toolkit_doctor`
- `run_materialscript`
- `get_gui_loop_status`
- `prepare_gui_submission_package`
- `read_module_result`
- `report_next_step`
- `publish_to_project_documents`

Practical note: this repo currently ships the local `pyproject.toml`, command modules, and package code, but not a separate polished release/install workflow beyond that. Treat the `pyproject.toml` as the source of truth for Python version, dependencies, and entrypoint names.

Editable-install note:

- `tools/ms_agent_toolkit/pyproject.toml` declares `package-dir = "../.."` for setuptools
- this is required because the `pyproject.toml` file lives under `tools/ms_agent_toolkit/`, while the import packages are rooted at the repository top level under `tools.*`

## Configuration on a new machine

Two config locations matter:

- Bridge config: `tools/ms_bridge/config/bridge_config.json`
- Toolkit config: `tools/ms_agent_toolkit/config/toolkit_config.json`

Fallback behavior:

- `run_materialscript` first looks for the concrete `*.json` files above
- if they do not exist, it falls back to:
  - `tools/ms_bridge/config/bridge_config.example.json`
  - `tools/ms_agent_toolkit/config/toolkit_config.example.json`

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
  - `guiLoopQueueRoot`
  - `guiLoopPollSeconds`
  - `guiLoopDefaultWaitSeconds`

### `RunMatScript.bat`

`RunMatScript.bat` is not included inside this repo. It comes from the local BIOVIA Materials Studio installation and is the main machine-specific setting to fix first.

Update `runMatScriptBat` in `tools/ms_bridge/config/bridge_config.json` so it points to the real local batch file, for example:

```json
"runMatScriptBat": "C:\\Program Files (x86)\\BIOVIA\\Materials Studio 24.1\\etc\\Scripting\\bin\\RunMatScript.bat"
```

Also review `materialsStudioInstallRoot` to match the installed version on that machine. If those paths are wrong, the PowerShell bridge at `tools/ms_bridge/scripts/invoke_materialscript.ps1` will fail before any MaterialsScript can run.

One more current-state note: `toolkit_config.json` / `toolkit_config.example.json` include `knowledgeRoot`, and this repo now ships `tools/ms_agent_toolkit/knowledge/` as a real delivered path.
That tree is curated from official Materials Studio docs and examples, and it helps the toolkit keep capability definitions and generated scripts aligned with the shipped API surface.
It supports better definition and script correctness, but it does not by itself make the toolkit a fully automatic execution engine.

## Command entrypoints

These names come directly from `tools/ms_agent_toolkit/pyproject.toml`.

### `run_materialscript`

Purpose: execute a compliant capability through either the standalone bridge path or the GUI-loop queue path and return a normalized execution result.

PowerShell-safe example:

```powershell
$params = '{"input_xsd":"C:/work/model.xsd","quality":"Fine"}'
run_materialscript --capability castep.energy --params-json $params
```

```powershell
$params = '{"input_xsd":"model.xsd","quality":"Fine"}'
run_materialscript --backend gui_loop --capability castep.geometry_optimization --params-json $params
```

```powershell
run_materialscript --capability castep.energy --params-file C:/work/params.json
```

Current behavior in the current branch:

- Reads a capability card from `tools/ms_agent_toolkit/capabilities/`
- Verifies required and allowed parameters
- Resolves the correct template
- Renders a real `.pl` script
- In `standalone` mode:
  - Writes `task_manifest.json`
  - Calls `tools/ms_bridge/scripts/invoke_materialscript.ps1`
  - Writes `run_result.json`
- In `gui_loop` mode:
  - Writes isolated workspace artifacts under the repo-local workspace tree
  - Copies the rendered script into `tools/gui_loop_queue/pending/`
  - Returns `stage: "task_queued"` with queue evidence paths
- Returns normalized execution output with evidence paths
- Accepts either `--params-json` or `--params-file`

Important `gui_loop` precondition:

- The current GUI geometry-optimization template reads `$Documents{...}` from the active Materials Studio GUI project.
- That means the input document name passed through `--params-json` must already exist in the GUI-visible project when `--backend gui_loop` is used for `castep.geometry_optimization`.
- The toolkit does not start the loop for you. A GUI-resident loop must already be running.
- The currently recommended loop implementation in this repo is `tools/gateway_agent_bridge/perl/gui_loop_v2.pl`.

### `prepare_gui_submission_package`

Purpose: generate a real GUI submission package on disk and return a normalized summary.

Example:

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package
```

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package --params-file C:/work/gui_params.json
```

Current behavior in the current branch:

- Returns `stage: "script_generated"`
- Copies the input `.xsd` into the output package directory
- Renders a real `.pl` file from the selected template
- Writes `task_manifest.json`
- Writes a package-local `README.md`
- Returns normalized artifact paths in the response
- Accepts either `--params-json` or `--params-file`

Template note for GUI geometry optimization:

- the template copies the GUI-visible source document into a separate working document through `SaveAs`
- the named result `.xsd` is therefore intended to represent the post-submission working document, not the untouched source document
- downstream result interpretation should still rely on the generated CASTEP result bundle, not only on the presence of the copied `.xsd`

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
- Returns `stage: "result_parsed"` with evidence paths, parsed result content, and:
  - `analysis.summary`
  - `analysis.status`
  - `analysis.nextStepOptions`

The intended agent loop is:

1. run a capability
2. read the result
3. inspect `analysis.summary`
4. present `analysis.nextStepOptions` to the human for the next run choice

### `report_next_step`

Purpose: turn one parsed result bundle into a fixed-shape round report for the human decision point after each run.

Example:

```powershell
report_next_step --module castep --result-dir C:/work/job42
```

Current behavior in the current branch:

- Reuses the same result parsing path as `read_module_result`
- Returns `stage: "round_report_ready"`
- Returns:
  - `analysis.summary`
  - `archiveRecommendation`
  - `nextExecutionPlan`
- This is the intended command for the "analyze this round and propose the next round" step

### `ms_agent_toolkit_doctor`

Purpose: run a static preflight over the local toolkit installation and configuration assumptions.

Example:

```powershell
ms_agent_toolkit_doctor
```

Current behavior in the current branch:

- Resolves the effective bridge and toolkit config paths
- Reports whether `RunMatScript.bat` exists at the configured location
- Reports whether `guiLoopQueueRoot` exists
- Explicitly states that this project is a CLI toolkit, not an MCP server

### `publish_to_project_documents`

Purpose: copy selected files into a target documents directory and return a normalized publication response.

Example:

```powershell
publish_to_project_documents --source-path C:/work/job42/output.xcd --source-path C:/work/job42/report.txt --project-documents-root C:/Projects/MyProject/Documents
```

Current behavior in the current branch:

- Returns `stage: "gui_publication_completed"`
- Copies each requested source file into the target documents directory
- Writes a publication `task_manifest.json`
- Returns the published file paths and manifest path

## Capability cards and templates

Capability cards live in:

- `tools/ms_agent_toolkit/capabilities/`

Current cards in this delivery:

- `castep.energy.json`
- `castep.geometry_optimization.json`
- `forcite.geometry_optimization.json`

Current-state detail: `forcite.geometry_optimization.json` is definition-complete, but the actual execution path is still not shipped in this release.

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
- Choose `standalone` or `gui_loop` execution intentionally
- Treat result `stage` values as execution-state signals
- Read `analysis.summary` and `analysis.nextStepOptions` after each completed parsing step
- Avoid treating the toolkit as a scientific decision engine

In practice, the skill file should be read together with:

- The capability card for the requested task
- The command wrapper being called
- The underlying `tools/ms_bridge/` scripts when actual execution behavior matters

Non-skill-capable agents can ignore `SKILL.md` and use this README plus the capability JSON files directly.

## Not included yet

This first version does not yet include:

- Result readers beyond `castep`
- An implemented `forcite.geometry_optimization` flow
- A shipped `tools/ms_agent_toolkit/knowledge/` directory that is delivered and used for capability and script guidance
- Experimental-mode command handling in the delivered CLI wrappers
- A full MCP server package under this toolkit directory
- Automatic startup control for the Materials Studio GUI loop itself

For actual backend execution and low-level bridge behavior, continue to inspect and reuse `tools/ms_bridge/`.
