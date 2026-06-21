from __future__ import annotations


def build_run_materialscript_command(
    invoke_script: str,
    runmatscript_bat: str,
    script_path: str,
    timeout_seconds: int,
    script_arguments: list[str],
) -> str:
    quoted_args = ",".join(f"'{arg}'" for arg in script_arguments)
    return (
        f"& '{invoke_script}' "
        f"-RunMatScriptBat '{runmatscript_bat}' "
        f"-ScriptPath '{script_path}' "
        f"-TimeoutSeconds {timeout_seconds} "
        f"-ScriptArguments @({quoted_args}) "
        f"-AsJson"
    )
