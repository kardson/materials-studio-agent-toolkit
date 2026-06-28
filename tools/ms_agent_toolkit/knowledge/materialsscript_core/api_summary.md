# MaterialsScript Core API Summary

## Scope
Materials Studio 24.1 ships the core scripting API help under `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\scriptingapi\` and the broader help portal under `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\MaterialsStudio.htm`.

## Summary
MaterialsScript automation is organized around a small shared object model: open or create a document, retrieve the module-specific task object, populate a `Settings(...)` block, and call `Run` on the task entry point. The core scripting API pages under `...\share\doc\content\scripting\scriptingapi\` are the quickest place to confirm document handles, collection traversal, and result access patterns before dropping into module-specific help.

For agent use, the important common rule is to treat the script as a thin orchestrator. Keep file paths explicit, pass only supported settings names into module calls, and read results from the returned study or result documents instead of inferring success from log text alone. Use `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\MaterialsStudio.htm` as the top-level index when you need to pivot from generic scripting behavior to a specific module reference page.
