# Forcite Parameter Guide

## Scope
Use the 24.1 Forcite scripting references such as `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\forcitescripting\apiforcite.htm` and `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\forcitescripting\apiforcitegeometryoptimization.htm`, with `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\MaterialsStudio.htm` as the index back into related help topics.

## Summary
Forcite parameters are easiest to curate in three groups: forcefield selection, task controls, and requested outputs. `apiforcite.htm` is the shared reference for module-level behavior and settings construction, while the geometry-optimization page is where you verify optimization-specific names, accepted values, and which controls are actually legal for that task.

For agent use, the main safeguards are to choose a forcefield that matches the system, keep convergence or quality controls explicit in the payload, and request only properties that will be consumed after the run. The official 24.1 pages remain the source of truth for exact identifiers, but this guide should emphasize operator decisions and validation checkpoints rather than copying raw option tables.
