# MaterialsScript Core API Summary

## Scope
Materials Studio 24.1 ships the shared scripting reference under `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\scriptingapi\` and the top-level help index at `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\MaterialsStudio.htm`.

## Summary
The core API is built around a consistent document-and-module model: open a project document, address structures and studies through document collections, obtain the module entry point, then execute a task with a `Settings(...)` block. The 24.1 scripting API pages are the canonical place to confirm object names, collection traversal, document saving rules, and the returned handles that later module-specific calls build on.

For toolkit work, the practical pattern is: keep paths explicit, validate parameter names against the module help before rendering a script, and treat returned documents or result objects as the source of truth for completion. Use `MaterialsStudio.htm` to jump from generic scripting behavior into module pages such as CASTEP or Forcite when a task-specific setting or result field needs confirmation.
