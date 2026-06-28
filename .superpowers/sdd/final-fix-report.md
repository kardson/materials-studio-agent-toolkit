# Final Fix Report - 2026-06-28

## Scope
- Updated `tools/ms_agent_toolkit/commands/run_materialscript.py` to reject non-execution-ready capabilities before template resolution.
- Added a focused regression test in `tools/ms_agent_toolkit/tests/test_run_materialscript_contract.py`.
- Replaced scaffold summaries in the flagged knowledge files with short curated 24.1 summaries.
- Strengthened `tools/ms_agent_toolkit/tests/test_knowledge_layout.py` to catch placeholder phrasing and require official source markers.

## Verification

### Focused run_materialscript test
Command:
```powershell
& '.\\.venv\\Scripts\\python.exe' -m unittest 'tools.ms_agent_toolkit.tests.test_run_materialscript_contract.BuildCompliantRequestTests.test_run_compliant_request_rejects_capability_without_supported_execution_modes'
```
Output:
```text
.
----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
```

### Knowledge layout module
Command:
```powershell
& '.\\.venv\\Scripts\\python.exe' -m unittest 'tools.ms_agent_toolkit.tests.test_knowledge_layout'
```
Output:
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
```

### Full toolkit suite
Command:
```powershell
& '.\\.venv\\Scripts\\python.exe' -m unittest discover -s 'tools/ms_agent_toolkit/tests'
```
Output:
```text
...........EEE..EE.....E..........
======================================================================
ERROR: test_enqueue_gui_loop_job_writes_workspace_artifacts_and_pending_script (test_gui_loop_runner.EnqueueGuiLoopRunnerTests.test_enqueue_gui_loop_job_writes_workspace_artifacts_and_pending_script)
PermissionError: [WinError 5] 拒绝访问。: 'C:\\Users\\kards\\Documents\\DFT_materials_studio_mcp_m1\\tools\\ms_agent_toolkit\\tests\\_gui_loop'

ERROR: test_read_gui_loop_job_state_prefers_status_json (test_gui_loop_runner.EnqueueGuiLoopRunnerTests.test_read_gui_loop_job_state_prefers_status_json)
PermissionError: [WinError 5] 拒绝访问。: 'C:\\Users\\kards\\Documents\\DFT_materials_studio_mcp_m1\\tools\\ms_agent_toolkit\\tests\\_gui_loop'

ERROR: test_get_status_returns_failed_state_from_status_json (test_gui_loop_status_command.GetGuiLoopStatusTests.test_get_status_returns_failed_state_from_status_json)
PermissionError: [WinError 5] 拒绝访问。: 'C:\\Users\\kards\\Documents\\DFT_materials_studio_mcp_m1\\tools\\ms_agent_toolkit\\tests\\_gui_loop_status'

ERROR: test_write_gui_package_injects_copied_input_name_when_parameters_omit_input_xsd (test_gui_submission_contract.BuildGuiManifestTests.test_write_gui_package_injects_copied_input_name_when_parameters_omit_input_xsd)
PermissionError: [Errno 13] Permission denied: 'C:\\Users\\kards\\Documents\\DFT_materials_studio_mcp_m1\\tools\\ms_agent_toolkit\\tests\\source_model.xsd'

ERROR: test_write_gui_package_materializes_expected_files (test_gui_submission_contract.BuildGuiManifestTests.test_write_gui_package_materializes_expected_files)
PermissionError: [Errno 13] Permission denied: 'C:\\Users\\kards\\Documents\\DFT_materials_studio_mcp_m1\\tools\\ms_agent_toolkit\\tests\\input.xsd'

ERROR: test_publish_files_copies_sources_and_writes_manifest (test_publication_contract.BuildPublicationResponseTests.test_publish_files_copies_sources_and_writes_manifest)
PermissionError: [WinError 5] 拒绝访问。: 'C:\\Users\\kards\\Documents\\DFT_materials_studio_mcp_m1\\tools\\ms_agent_toolkit\\tests\\_publish'

----------------------------------------------------------------------
Ran 34 tests in 0.023s

FAILED (errors=6)
```

## Notes
- The targeted regression test and the updated knowledge-layout module both pass.
- The required full toolkit run was executed once and is currently blocked by existing write-permission assumptions in unrelated tests that materialize files under `tools/ms_agent_toolkit/tests`.
