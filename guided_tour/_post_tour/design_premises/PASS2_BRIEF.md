# Design premises verification, pass 2: independent re-check (approved by the operator, 2026-11-04)

Read BRIEF.md in this folder first (same rules). Pass 1 gave each design finding's premises a
verdict. For every row of your p_batch file(s) whose verdict is PREMISES HOLD, PARTLY HOLD or
PREMISE FALSE: re-read the inspector's item, verify its premises FROM SCRATCH before reading pass 1's
evidence, then try to prove pass 1 wrong (a missed reader, a flag that changes reachability, a
misread line, an overstated "never"/"always"/"no code"). Rows marked PURE JUDGMENT or NOT CHECKABLE
HERE: check only that the label is right.

Pass-2 verdict per row: UPHELD; AMENDED (verdict stands, but the premises list or correct fact
needed a fix: give it); CHANGED TO <verdict> (give the right verdict and why).

Write ONLY design_premises/pass2_<NN>.md:
# Design premises pass 2, batch(es) <NN>
| ID | Pass-1 verdict | Pass-2 verdict | Evidence / amendment (file:line, searches) |
|---|---|---|---|
One row per row of your p_batch file(s). No "|" inside a cell. Then "## Not checked". Facts only.
