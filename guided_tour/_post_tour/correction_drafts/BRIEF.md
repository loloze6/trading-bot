# Correction drafts: brief (approved by the operator, 2026-11-04)

## Purpose
The disagreements verification (../disagreements/disagreements_verification.md) lists, in its
section "Candidate corrections", the items whose final verdict is SPEECH WRONG, SPEECH INCOMPLETE or
PARTLY. Under the tour's rules (guided_tour/00_guide_opening_prompt.md section 7 and
00_rectifications.md rectification 2 point 3), a speech that was wrong on a fact gets a
"Correction (<date>)" paragraph under that stop's Speech section; the speech itself is never
rewritten. You DRAFT those paragraphs, in a separate file. Nothing is applied to any stop file: the
direction session or the operator rules first.

## Model
The existing correction in guided_tour/01_the_brief.md (the paragraph starting
"**Correction (2026-10-29).**", just above "## Operator remarks"). Same form: bold label, then what
the speech said, then what the files say, with file:line. Leave the date as "<date>".

## Per candidate item
1. Read the candidate row: the disagreement, the final verdict, pass 1's correct fact, and pass 2's
   column (where pass 2 says CORRECT FACT AMENDED or CHANGED, pass 2's fact wins).
2. Read the disputed part of the stop's Speech (and reading map) and check the correct fact against
   the files yourself (real lines). If you find the correct fact is itself wrong, say so and do not
   draft: mark it "NOT DRAFTED: <why>".
3. Draft one short paragraph per item, in plain words (rectification 1: business first; file:line
   in brackets is fine in a correction). Group several items of the same stop into one
   "Correction (<date>)" block with numbered points if they touch the same part.
4. Line-drift-only items are NOT candidates; skip anything not in the candidate list.

## Output
Write ONLY correction_drafts/drafts_<NN>.md:

# Correction drafts, stops <list>
## Stop NN
Items: <IDs>
**Correction (<date>).** <text>
(repeat per stop)

## Not drafted
<ID>: <why>

## Hard rules
Same as ../BRIEF.md "Hard rules" (read-only except your file; no dates from the data policy, no
window labels; never open TB/local_data/, holdout_sealed, composite/, quarantine/). Do not edit stop
files. No design proposals: a correction states a fact, nothing else.
