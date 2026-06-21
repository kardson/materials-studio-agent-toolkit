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
4. Execute or package the result.

## Experimental Path

1. Use `--experimental`.
2. Provide a script file or script content directly.
3. Review evidence artifacts after execution.

## Result Handling

1. Use `read_module_result` after execution artifacts exist.
2. Interpret `stage` before drawing conclusions.
3. Treat `result_parsed` as the only stage suitable for scientific interpretation.

## After Execution

1. Use parsed results to compare outcomes.
2. Decide the next modeling or calculation step from the parsed evidence.
3. Do not treat the toolkit as a scientific decision engine; it prepares structured evidence for the agent.
