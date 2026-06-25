from __future__ import annotations


def build_result_analysis(module: str, parsed_result: dict) -> dict:
    status = parsed_result.get("status", "unknown")
    task = parsed_result.get("task")
    final_energy = parsed_result.get("finalEnergyEv")
    total_time = parsed_result.get("totalTimeSeconds")

    if status == "completed":
        summary = (
            f"{module.upper()} {task or 'calculation'} completed"
            + (f"; final energy = {final_energy} eV" if final_energy is not None else "")
            + (f"; total time = {total_time} s" if total_time is not None else "")
        )
        next_step_options = [
            {
                "optionId": "archive_and_compare",
                "title": "Archive and compare",
                "reason": "Result is complete and suitable for publication or cross-run comparison.",
            },
            {
                "optionId": "refine_settings",
                "title": "Run a refinement calculation",
                "reason": "A successful baseline run can be followed by finer quality settings or a denser k-point setup.",
            },
        ]
    elif status == "failed":
        summary = f"{module.upper()} {task or 'calculation'} failed; inspect output and adjust settings before retry."
        next_step_options = [
            {
                "optionId": "inspect_failure",
                "title": "Inspect failure details",
                "reason": "Failure should be diagnosed from the generated result bundle before re-running.",
            },
            {
                "optionId": "retry_with_safer_settings",
                "title": "Retry with safer settings",
                "reason": "A reduced quality or simpler setup is often the next controlled experiment after a failure.",
            },
        ]
    else:
        summary = f"{module.upper()} {task or 'calculation'} result state is unknown; gather more evidence before the next run."
        next_step_options = [
            {
                "optionId": "inspect_result_bundle",
                "title": "Inspect result bundle",
                "reason": "The parser could not confirm completion or failure from the available files.",
            }
        ]

    return {
        "summary": summary,
        "status": status,
        "nextStepOptions": next_step_options,
    }
