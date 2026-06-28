# Materials Studio Agent Toolkit

## When to Use

Use this toolkit when you need to generate `MaterialsScript`, package formal GUI submissions, parse Materials Studio calculation results, or publish outputs into project documents.

## Capability Selection

1. Prefer a matching capability card first.
2. Use compliant mode when a capability exists.
3. Use experimental mode only when no approved capability fits.

## Compliant Path

1. Select a capability.
2. Pass required values through `--params-json`.
3. Let the toolkit render an approved template.
4. Choose the execution surface deliberately:
   - use the default standalone backend for direct `RunMatScript.bat` execution
   - use `run_materialscript --backend gui_loop` when a Materials Studio GUI-resident loop is already running
5. Execute or package the result.

## Experimental Path

1. Use `--experimental`.
2. Provide a script file or script content directly.
3. Review evidence artifacts after execution.

## Result Handling

1. Use `read_module_result` after execution artifacts exist.
2. Interpret `stage` before drawing conclusions.
3. Treat `result_parsed` as the only stage suitable for scientific interpretation.
4. After parsing, read `analysis.summary` and `analysis.nextStepOptions`.
5. Present both the analysis and the candidate next-step plan to the human before launching the next run.

## After Execution

1. Use parsed results to compare outcomes.
2. Use `analysis.summary` as the structured one-paragraph conclusion for the current run.
3. Use `analysis.nextStepOptions` as the shortlist of next execution plans for the human to choose from.
4. Do not treat the toolkit as a scientific decision engine; it prepares structured evidence for the agent.

## Command Examples

```powershell
ms_agent_toolkit_doctor
```

```powershell
$params = '{"input_xsd":"C:/work/model.xsd","quality":"Fine","cutoff_energy":"450 eV","kpoint_grid":"2 2 2"}'
run_materialscript --capability castep.energy --params-json $params
```

```powershell
run_materialscript --capability castep.energy --params-file C:/work/params.json
```

```powershell
read_module_result --module castep --result-dir C:/work/job42
report_next_step --module castep --result-dir C:/work/job42
```

```powershell
publish_to_project_documents --source-path C:/work/job42/output.xcd --source-path C:/work/job42/report.txt --project-documents-root C:/Projects/MyProject/Documents
```
