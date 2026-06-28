# CASTEP Parameter Guide

## Scope
Use the 24.1 CASTEP scripting and setup pages such as:

- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicastepenergy.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\castepscripting\apicastepgeometryoptimization.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\modules\castep\dlgcastepcalcsetup.htm`
- `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\modules\castep\dlgcastepgeomopt.htm`

## Summary
For the current toolkit, the safest CASTEP parameter groups are:

### 1. Calculation quality

- `Quality`
Meaning:
selects the overall preset controlling accuracy/speed tradeoffs.

Typical values:
- `Coarse`
- `Medium`
- `Fine`

Recommendation:
use `Coarse` or `Medium` for exploratory screening and `Fine` only when the user is intentionally refining a promising structure.

### 2. Plane-wave cutoff

- `CutoffEnergy`
Meaning:
sets the plane-wave basis cutoff. Higher values generally improve accuracy but increase cost.

Recommendation:
only expose this when the user explicitly wants basis refinement. If omitted, prefer the built-in quality preset first. When both `Quality` and `CutoffEnergy` are present, treat `CutoffEnergy` as an explicit override requiring more careful convergence checking.

### 3. k-point sampling

- `KPointMPGrid`
Meaning:
defines the Monkhorst-Pack k-point grid for periodic systems.

Recommendation:
this matters mainly for crystals and slabs. Molecular-in-box systems often do not need dense k-point sampling. Expose this only when the structure is periodic or when the user is doing convergence work.

### 4. Geometry-optimization-specific controls

- `CellOptimization`
Meaning:
controls whether only atoms move or whether the unit cell is also optimized.

Recommendation:
use atomic-only optimization unless the user explicitly wants lattice relaxation. Full cell optimization changes both structure and lattice and should be treated as a more invasive step.

### 5. Property requests

- `CalculateDOS`
- `CalculateBandStructure`
- `CalculateChargeDensity`

Meaning:
request extra post-run properties in addition to the main task.

Recommendation:
do not enable extra properties by default. Request only the outputs the downstream reader or user actually needs, because each additional property increases runtime and output complexity.
