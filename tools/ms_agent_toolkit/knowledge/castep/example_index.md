# CASTEP Example Index

## Scope
The shipped 24.1 CASTEP examples under `C:\Program Files (x86)\BIOVIA\Materials Studio 24.1\share\Examples\Projects\CASTEP\` are the fastest way to inspect known-good study layouts, generated files, and result naming.

## Summary
`Fe_phonons.stp` is the most compact reference for a complete phonon workflow: it shows how a CASTEP study stores structure inputs, calculation settings, and the downstream files associated with vibrational analysis. It is the right first check when you need to understand what a successful multi-step CASTEP study leaves behind.

`l_alanine.stp` is a better comparison point for molecular or low-symmetry systems because it exercises a more chemistry-oriented structure and a settings mix that is sensitive to convergence choices. Use these example projects together with the 24.1 CASTEP scripting help to confirm study naming conventions, expected result bundle contents, and which output artifacts are stable enough for downstream readers to rely on.
