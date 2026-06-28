# Forcite Parameter Guide

## Scope
Use the 24.1 Forcite scripting pages such as `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\forcitescripting\apiforcitegeometryoptimization.htm` and `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\content\scripting\forcitescripting\apiforcite.htm` together with the broader help portal at `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\doc\MaterialsStudio.htm`.

## Summary
Forcite setup decisions are easiest to reason about in three buckets: forcefield selection, geometry or dynamics controls, and requested properties. The geometry optimization entry point is where you confirm optimization-specific settings and acceptable parameter names, while the broader `apiforcite.htm` page is the better anchor for shared module behavior such as constructing settings blocks and choosing task families.

When curating agent guidance, prefer short reminders over raw option dumps: verify that the forcefield is compatible with the document contents, keep convergence or quality settings explicit in the script payload, and request only the properties you plan to read back. The official 24.1 pages above are the source of truth for exact identifiers, but the agent summary should stay focused on decision support rather than mirroring help text.
