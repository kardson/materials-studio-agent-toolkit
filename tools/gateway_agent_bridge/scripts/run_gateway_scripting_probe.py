from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.gateway_agent_bridge.scripts.manage_gateway_job import parse_create_job_stdout, parse_simple_ok, write_json
from tools.gateway_agent_bridge.scripts.query_gateway_job import parse_gateway_status_text


def call_gateway(invoke_script: str, action: str, args: list[str]) -> dict:
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        f"& '{invoke_script}' -GatewayAction '{action}' -Arguments @({','.join([repr(x) for x in args])}) -AsJson",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(completed.stdout)


def create_job(invoke_script: str, user_id: str) -> str:
    response = call_gateway(invoke_script, "DSD_CreateJob", [f"server=Scripting", f"userid={user_id}"])
    parsed = parse_create_job_stdout(response["stdout"])
    job_id = parsed["jobId"]
    if not job_id:
        raise RuntimeError("Gateway did not return a job-id")
    return job_id


def add_job_info(invoke_script: str, job_id: str, modifier: str, arguments: str) -> dict:
    return call_gateway(
        invoke_script,
        "DSD_ADDJOBINFO",
        [f"job-id={job_id}", f"modifier={modifier}", f"arguments={arguments}"],
    )


def add_message(invoke_script: str, job_id: str, msg_type: str, modifier: str, arguments: str) -> dict:
    return call_gateway(
        invoke_script,
        "DSD_ADDMESSAGE",
        [f"job-id={job_id}", f"type={msg_type}", f"modifier={modifier}", f"arguments={arguments}"],
    )


def submit_job(invoke_script: str, job_id: str) -> dict:
    return call_gateway(invoke_script, "DSD_SUBMITJOB", [f"job-id={job_id}", "local=true"])


def query_job_status(invoke_script: str, job_id: str) -> dict:
    response = call_gateway(invoke_script, "DSD_GETJOBSTATUS", [f"job-id={job_id}"])
    status_payload = parse_gateway_status_text(job_id=job_id, status_text=response["stdout"])
    return {
        "response": response,
        "statusPayload": status_payload,
    }


def prepare_probe_job_files(job_id: str, jobs_root: str, template_name: str, script_name: str) -> dict:
    job_dir = Path(jobs_root) / job_id
    script_file = job_dir / script_name
    template_path = Path(__file__).resolve().parents[1] / "perl" / template_name
    script_file.write_text(template_path.read_text(encoding="utf-8"), encoding="ascii")
    (job_dir / "LastUploadFile.txt").write_text("", encoding="ascii")
    return {
        "jobDir": str(job_dir),
        "scriptFile": str(script_file),
        "lastUploadFile": str(job_dir / "LastUploadFile.txt"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal Gateway scripting probe job.")
    parser.add_argument("--invoke-script", required=True)
    parser.add_argument("--jobs-root", required=True)
    parser.add_argument("--user-id", default="codex")
    parser.add_argument("--output", required=True)
    parser.add_argument("--template-name", default="submit_scripting_probe_template.pl")
    parser.add_argument("--script-name", default="GatewayScriptingProbe.pl")
    parser.add_argument("--job-label", default="GatewayScriptingProbe")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    job_id = create_job(args.invoke_script, args.user_id)
    files = prepare_probe_job_files(job_id, args.jobs_root, args.template_name, args.script_name)
    add_job_info(args.invoke_script, job_id, "job-description", args.job_label)
    add_message(args.invoke_script, job_id, "custom", "RunMode", "ScriptingFlat")
    add_message(args.invoke_script, job_id, "custom", "SeedName", args.job_label)
    add_message(args.invoke_script, job_id, "custom", "job-name", args.job_label)
    add_message(args.invoke_script, job_id, "custom", "run-item", f"{args.job_label}!")
    add_message(args.invoke_script, job_id, "custom", "ScriptArguments", args.job_label)
    submit = submit_job(args.invoke_script, job_id)
    status = query_job_status(args.invoke_script, job_id)
    payload = {
        "jobId": job_id,
        "files": files,
        "submit": parse_simple_ok("DSD_SUBMITJOB", submit["stdout"]),
        "status": status["statusPayload"],
        "rawStatusResponse": status["response"],
    }
    write_json(args.output, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
