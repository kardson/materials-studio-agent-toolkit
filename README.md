# Materials Studio Agent Toolkit

`materials-studio-agent-toolkit` is a public, local-first toolkit for helping agents work with BIOVIA Materials Studio through structured scripts, capability cards, templates, and result readers.

It is designed for the case where an agent shares a machine or workspace with a human operator and needs to:

1. generate `MaterialsScript` from approved capability definitions
2. prepare formal GUI submission packages
3. read and normalize calculation results
4. publish selected outputs into project documents

This repository does **not** expose an MCP server. The current delivery is a lightweight CLI toolkit plus a generic `SKILL.md`.

## What this repository contains

### Core toolkit

The main delivery lives under:

- [tools/ms_agent_toolkit](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit)

It includes:

- capability registry loader and JSON capability cards
- Jinja2 `.pl.j2` templates
- command wrappers
- thin adapters
- contract tests
- mock fixtures
- package metadata in [pyproject.toml](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit/pyproject.toml)
- delivery README in [tools/ms_agent_toolkit/README.md](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit/README.md)

### Generic skill guide

The agent-facing generic skill guide lives at:

- [skills/materials-studio-agent-toolkit/SKILL.md](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/skills/materials-studio-agent-toolkit/SKILL.md)

Use this with any skill-capable agent that can read or import a `SKILL.md` file.

### Supporting bridge utilities

This repo also includes the validated bridge layer that the toolkit currently wraps:

- [tools/ms_bridge](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_bridge)

Reference-only historical or supporting Materials Studio automation assets are also present here:

- [tools/gateway_agent_bridge](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/gateway_agent_bridge)

## First-release status

The current release includes:

- CLI command entrypoints declared in `pyproject.toml`
- static capability cards for:
  - `castep.energy`
  - `castep.geometry_optimization`
  - reserved `forcite.geometry_optimization`
- first-release templates for:
  - standalone CASTEP energy
  - GUI CASTEP geometry optimization
- result reading support for `castep`
- a generic skill guide
- passing toolkit tests
- passing legacy `ms_bridge` tests

Important current-state limitation:

- the command wrappers in this release still focus on **structured request generation, packaging metadata, result normalization, and publication response shaping**
- they do **not** yet provide a complete one-shot execution orchestrator that generates, runs, monitors, and publishes a full Materials Studio workflow end to end

## Quick start

### Python requirements

From [tools/ms_agent_toolkit/pyproject.toml](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit/pyproject.toml):

- Python `>=3.12`
- `pydantic>=2.0`
- `jinja2>=3.1`

### Install locally

From the repository root:

```powershell
py -3.12 -m pip install -e .\tools\ms_agent_toolkit
```

### Main commands

Declared console entrypoints:

- `run_materialscript`
- `prepare_gui_submission_package`
- `read_module_result`
- `publish_to_project_documents`

Example usage:

```powershell
run_materialscript --capability castep.energy --params-json "{\"input_xsd\":\"C:/work/model.xsd\",\"quality\":\"Fine\"}"
```

```powershell
prepare_gui_submission_package --capability castep.geometry_optimization --input-xsd C:/work/model.xsd --output-dir C:/work/gui_package
```

```powershell
read_module_result --module castep --result-dir C:/work/job42
```

```powershell
publish_to_project_documents --source-path C:/work/job42/output.xcd --source-path C:/work/job42/report.txt --project-documents-root C:/Projects/MyProject/Documents
```

## Machine setup

This repo does **not** bundle `RunMatScript.bat`. That comes from the local Materials Studio installation.

Before using backend execution paths, review:

- [tools/ms_bridge/config/bridge_config.example.json](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_bridge/config/bridge_config.example.json)
- [tools/ms_agent_toolkit/config/toolkit_config.example.json](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit/config/toolkit_config.example.json)

In particular, fix:

- `materialsStudioInstallRoot`
- `runMatScriptBat`
- `workspaceRoot`
- `defaultProjectDocumentsRoot`
- `capabilityRegistryPath`
- `templatesRoot`

If `runMatScriptBat` is wrong, the toolkit cannot launch MaterialsScript through the existing bridge.

## How to give this to another agent

### For a skill-capable agent

Provide:

- [skills/materials-studio-agent-toolkit/SKILL.md](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/skills/materials-studio-agent-toolkit/SKILL.md)
- the whole [tools/ms_agent_toolkit](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit) directory
- the wrapped backend utilities under [tools/ms_bridge](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_bridge)

The agent should read `SKILL.md`, then follow the command and capability flow described there.

### For a non-skill-capable agent

Provide:

- this repository
- [tools/ms_agent_toolkit/README.md](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit/README.md)
- the command-line entrypoints
- the capability JSON files

In that scenario, the agent can operate directly through the CLI wrappers and capability files.

## Repository structure

Main areas:

- [tools/ms_agent_toolkit](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_agent_toolkit)
- [tools/ms_bridge](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/tools/ms_bridge)
- [skills/materials-studio-agent-toolkit](C:/Users/kards/Documents/DFT_materials_studio_mcp_m1/skills/materials-studio-agent-toolkit)

## What is not included yet

This public repository does not yet include:

- an MCP server
- a full one-shot execution orchestrator
- non-CASTEP result readers
- a completed Forcite execution path
- a shipped knowledge pack directory under `tools/ms_agent_toolkit/knowledge`
- experimental-mode command implementations in the current CLI wrappers

## Validation status

At the time of publication:

- toolkit test suite passed
- `ms_bridge` test suite passed

The toolkit is therefore published as a working first-release engineering artifact, not merely a design stub.
