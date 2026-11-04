# Disagreements verification, pass 2: independent re-check (approved by the operator, 2026-11-04)

Read BRIEF.md in this folder first (same repo, flag set, checkout limits and hard rules).

## Your job
Pass 1 gave each inspector disagreement item a verdict. Some verdicts will lead to a dated
"Correction" under a stop's speech (speech wrong / incomplete); others dismiss the inspector's claim
(inspector wrong). Both need an independent re-check. For each row of your d_batch file(s):

0. First classify the item. If the inspector's item states no disagreement (it only confirms the
   speech, e.g. "verified as stated", "correct", "matches"), and that confirmation holds, the pass-2
   verdict is NO DISAGREEMENT, and you move on. Pass 1 labelled such items inconsistently
   (INSPECTOR WRONG tagged "confirms speech", SPEECH RIGHT, or PARTLY).
1. Otherwise, if pass 1's verdict is SPEECH WRONG, SPEECH INCOMPLETE, PARTLY or INSPECTOR WRONG:
   read the inspector's item and the disputed part of the speech (and its reading map), then verify
   FROM SCRATCH against the files before reading pass 1's evidence, so you are not anchored.
   Try to prove pass 1 wrong.
2. Rows with LINE DRIFT ONLY or NOT CHECKABLE HERE: check only that the label is right (a quick look);
   do not redo them in depth.
3. Pass-2 verdict:
   - NO DISAGREEMENT (step 0).
   - UPHELD: pass 1's verdict and correct fact stand.
   - CORRECT FACT AMENDED: verdict stands, but pass 1's "correct fact" is inaccurate or incomplete;
     give the amended fact with file:line.
   - CHANGED TO <verdict>: pass 1's verdict is wrong; give the right one from BRIEF.md's list and why.

## Output
Write ONLY pass2_<NN>.md in this folder (NN given in your task). Do not edit d_batch files or stop
files.

# Disagreements pass 2, batch(es) <NN>
| ID | Pass-1 verdict | Pass-2 verdict | Evidence / amended fact (file:line, searches) |
|---|---|---|---|

Every row of your d_batch file(s) gets a row here. Do not use "|" inside a cell. Then "## Not
checked". Facts only, no proposals, no dates.
