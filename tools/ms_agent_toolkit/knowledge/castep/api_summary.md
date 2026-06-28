# CASTEP API Summary

## Scope
Materials Studio 24.1 documents the CASTEP scripting entry points under:

- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicasteprunenergy.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicasteprungeometryoptimization.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicastep.htm`

## Summary
For the current toolkit, the two core execution entry points are:

- `Modules->CASTEP->Energy->Run(<system>, <settings>)`
- `Modules->CASTEP->GeometryOptimization->Run(<system>, <settings>)`

Both expect a 3D Atomistic document, atom, or atom group as the first argument and an optional `Settings(...)` block as the second argument. In practice, the toolkit should treat CASTEP scripts as thin orchestration wrappers: resolve the input document, build a small explicit settings block, call the task, then read authoritative outputs from the returned result object and generated CASTEP files.

The returned results object is the first structured signal of success. For energy runs, the official docs expose at least the updated `Structure` and `Report`, plus scalar result values such as total energy, free energy, magnetic moment, and band gap when those quantities are available. For geometry optimization runs, the official docs expose the updated `Structure`, a text `Report`, and convergence-related values such as `Converged`, `TotalEnergy`, and `Enthalpy`.
