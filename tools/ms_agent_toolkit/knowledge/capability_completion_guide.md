# Missing Knowledge And Capability Completion Guide

## Purpose

Use this guide when the toolkit does not already ship the module knowledge or capability card needed for the current task.

The guiding rule is simple:

- always work from the local official Materials Studio installation
- never invent a new capability or template from memory alone

The expected local reference roots are:

- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\Examples`

## Completion Order

When something is missing, complete it in this order:

1. knowledge
2. capability definition
3. template
4. execution wiring
5. result reading

Do not jump directly to execution if the earlier layers are absent.

## Step 1: Check What Already Exists

Before adding anything new, inspect:

- `tools/ms_agent_toolkit/capabilities/`
- `tools/ms_agent_toolkit/knowledge/`
- `tools/ms_agent_toolkit/templates/`

If an equivalent module or task already exists, extend the existing material instead of creating a parallel duplicate.

## Step 2: Build The Knowledge Layer First

If module knowledge is missing, create or update:

- `knowledge/<module>/api_summary.md`
- `knowledge/<module>/parameter_guide.md`
- `knowledge/<module>/result_semantics.md`
- `knowledge/<module>/example_index.md`

Use the official documentation tree for:

- API signatures
- object names
- parameter names
- module task names

Use the official examples tree for:

- runnable reference scripts
- project structure
- file and document handling patterns

Keep the knowledge files curated and short. They should summarize official behavior, not copy whole help pages.

## Step 3: Add Or Upgrade The Capability Card

Once the knowledge layer exists, create or upgrade the capability card.

A definition-complete capability card includes:

- `capability_id`
- `module`
- `task`
- `official_api_signature`
- `official_doc_refs`
- `official_example_refs`
- `template_id`
- `allowed_parameters`
- `required_inputs`
- `result_reader`
- `supported_execution_modes`
- `notes`

If execution is not yet ready, keep:

- `supported_execution_modes: []`

and say so explicitly in `notes`.

## Step 4: Promote To Execution-Ready Only When All Pieces Exist

A capability is execution-ready only if all of these exist:

- a normalized template
- an approved execution mode
- command wiring
- result interpretation path
- tests

If any of those are missing, do not mark the capability as runnable.

## Step 5: Source Discipline

Use only official local Materials Studio sources provided by the user or present on the machine.

Preferred source types:

1. official scripting help pages under `share\doc\content\scripting\`
2. official example scripts and example projects under `share\Examples\`

Do not use:

- memory-only API guesses
- random online tutorials
- non-authoritative screenshots as primary references when a help page exists

## Expected Output States

There are three valid states for a capability:

- `definition-complete`
- `template-approved`
- `execution-ready`

Do not collapse these states into one.

The toolkit is safer when it can say:

- “this capability is understood”

without falsely saying:

- “this capability is executable”
