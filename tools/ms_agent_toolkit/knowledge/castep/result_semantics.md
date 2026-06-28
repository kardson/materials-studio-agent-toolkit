# CASTEP Result Semantics

## Scope
The official CASTEP task docs and example projects, especially:

- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicasteprunenergy.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicasteprungeometryoptimization.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicastepfiles.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\Examples\Projects\CASTEP\Fe_phonons.stp`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\Examples\Projects\CASTEP\l_alanine.stp`

illustrate the result shapes the toolkit should treat as authoritative.

## Summary
The toolkit should rank CASTEP outputs by trust level:

### 1. Primary scientific evidence

- `*.castep`
- `*.param`

These are the main text outputs for downstream parsing. The `.castep` file carries run narrative, convergence information, timing, and values such as final energy. The `.param` file captures the parameter state used for the run. For lightweight post-run reasoning, these two files are the minimum authoritative pair.

### 2. Returned MaterialsScript result object

When the run is executed through the scripting API, the returned results object may expose:

- `Structure`
- `Report`
- scalar values such as `TotalEnergy`, `FreeEnergy`, `Converged`, or `Enthalpy`

This is useful for immediate script-level branching, but the toolkit should still preserve the generated CASTEP files because they are easier to archive, compare, and re-parse later.

### 3. Updated structure documents

- returned `Structure`
- copied or saved `.xsd`

These are useful convenience artifacts for the final geometry, but they are not sufficient by themselves to prove scientific success. A geometry file without matching `.castep` and `.param` evidence should not be treated as a completed CASTEP result bundle.

### 4. Completion signal

For the current toolkit reader, the safest completed-run signal is:

- a readable `.castep` file
- a readable `.param` file
- parsable final energy and runtime markers, or another module-specific convergence marker

If those are missing, the run should be treated as failed or unknown even if a structure file exists.
