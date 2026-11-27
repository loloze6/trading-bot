# Build B11 and B12 (2026-11-27, branch `build-b11-b12`)

The operator's go: next steps B11 and B12 (`topics/NEXT_STEPS.md`), evidence `topics/47_review/night9_review.py`, `.txt`.

## Purpose
- **B11.** Money goes to ideas that may still prove real, not to effects the data shows absent: step 5 gets a third
  answer, **no effect** (enough cases, the effect near zero or pointing the other way), which goes to line 7.c;
  "rejected" joins it; "inconclusive" (unclear) keeps its meaning and goes to 7.b.
- **B12.** A repair is tried where it can reach the bar: line 7.d runs only on a confirmed, unprofitable strategy that
  fails at most 2 of step 6's 6 measures.

## Expected outcomes (written before the build)
- B11, step 5 rerun with each plan's stored `measure.py` on night 9's tested ideas (no model call): only the unclear
  answers with t below 1, and the rejected one, become "no effect"; nothing else changes. Night 9's count is checked
  against `night9_review.txt` part 3 (that part counts nights 7 to 9 together).
- B12, on night 9's tables: the 7.d calls the new entry condition would have skipped led to 0 profitable strategies.
- Both: `run_idea` on one seeded idea whose answers do not change gives the same files with the new code as without.
- The cards' tests and the bot's tests pass.

## Where the status is decided
Step 5's status comes from the model-written `measure.py` (the plan's three rules). "No effect" is therefore decided
afterwards, in step 5's own code (`make_verdict.py`, `effect_check`), after the direction check: one place, in code,
not in a prompt. The model's prompt is unchanged.

**One correction to the evidence's reading.** `night9_review.py` reads the t as recorded. For a plan whose confirm rule
is `t ≤ -2` (a falling slope), a recorded t of -1.8 is a sign of the effect, not its absence. The rule counts the t in
the idea's direction: the sign of the first t threshold in the plan's "Confirm:" line (540 of 540 plans of nights 7 to
9 have one; 21 are `t ≤ -2`).

## What was built (files)
| File | Change |
|---|---|
| `common/verdicts.md` (new), `common/README.md` | the five answers; the rule of "no effect"; an old "rejected" read as "no effect" |
| `common/lib.py` | `STEP5_ANSWERS`, `step5_answer()` (old words read today) |
| `05_verification/helper/make_verdict.py` | `idea_direction()`, `effect_check()`: status "no effect"; `effect_check` in `result.json`, one line in `verdict.md`, a sentence added to "decided by" |
| `05_verification/card.md` | the answer defined, the field, the code check |
| `07c_rejected/helper/line.yaml`, `line_prompt.md`, `card.md` | entry `no effect`; the prompt's first two lines say "no effect" (folder name kept: its runs are under it) |
| `07b_inconclusive/card.md` | what "inconclusive" means since B11 (its prompt unchanged) |
| `07d_not_profitable/helper/line.yaml`, `card.md` | B12: `step6_failed_at_most: 2`, with the evidence |
| `07_common/helper/analyse.py`, `07_common/card.md` | `entry_met` reads `step6_failed_at_most` (new `failed_of`: the measures step 6 failed); step 5's answer read through `step5_answer`; the index line of a line not run names the failed count |
| `orchestration/run_idea/helper/run_idea.py` | `verdict_label` reads through `step5_answer` (one line) |
| `run_viewer/helper/build_page.py`, `page.html`, `card.md` | "no effect" in the order and colours; old "rejected" shown as "no effect"; help texts. `runs.html` not rebuilt |
| tests: `test_make_verdict.py`, `test_analyse.py` | the rule, the direction, 7.c's and 7.d's entries, `failed_of` |
| `runs/build_b11_b12/` | the proofs' scripts and their outputs |

Readers checked and left unchanged (they test "confirmed" or "profitable enough" only, or copy the status):
`chart_files.worth_a_chart`, `select_next`, `loop`, `ideas_similarities_check`, `common_record`, `unseen_test`,
`combine/judge_unseen`. **Shared files touched with the other builds:** none of `orchestration/select_next/`,
`orchestration/loop/`, `orchestration/run_brief/`, nor 7.g's call or prompt. Touched and shared by every line:
`07_common/helper/analyse.py` (entry condition), `common/lib.py` (one function added), `run_idea.py` (one line).
