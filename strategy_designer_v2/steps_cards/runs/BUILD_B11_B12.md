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

## Proofs, with counts
**B11, part 1: the rule on every stored result** (`build_b11_b12/b11_count.py`; outputs `b11_count_night9.txt`,
`b11_count_nights789.txt`). The rule reads only `result.json` and the plan, so it is applied, as `make_verdict.py`
applies it, to each stored result. Not done as written: rerunning all 184 stored `measure.py` needs every record's bars,
which are not committed; rebuilding them is night 9's step 4 again, 21.8 hours. Part 2 shows the rerun reproduces.

| Night 9, 184 tested ideas | count |
|---|---|
| confirmed, unchanged | 58 |
| inconclusive, unchanged | 67 |
| **inconclusive -> no effect** | **55** |
| mismatch, not observable, unchanged | 2, 2 |
| rejected | 0 (none on night 9) |

Against `night9_review.py`'s reading on night 9 alone: 55 unclear with the recorded t below 1, 67 at 1 or more; the
55 that change are exactly those 55. Nights 7 to 9 (474 rows with a result): 148 unclear and the 1 rejected
(night 8, 069-01) become no effect; 151 unclear have a recorded t below 1, and the 3 that stay unclear are plans whose
confirm rule is `t ≤ -2` (recorded t -1.47, -2.92, -1.70: towards the idea). As expected, but for those 3.

**B11, part 2: the stored measure.py rerun** (`build_b11_b12/b11_sample.sh`, `b11_sample_result.txt`): three night 9
plans, step 4 rebuilt in a scratch folder, step 5 with the stored `measure.py` (no model call). Every number of
`result.json` is identical to the committed one; only the new rule's fields differ.

| Plan | committed -> rerun | fields that differ |
|---|---|---|
| 072-01 (confirm `t ≤ -2`) | inconclusive -> no effect (t in the idea's direction -0.099, 1,901 cases) | status, decided_by, effect_check |
| 072-03 | inconclusive -> no effect (+0.037, 1,885 cases) | status, decided_by, effect_check |
| 072-02 | inconclusive -> inconclusive (+1.868, 1,691 cases) | effect_check |

**B12** (`build_b11_b12/b12_count.py`; `b12_count_night9.txt`, `b12_count_nights789.txt`): the 7.d calls of the tables
(the line ran on the backtest), each parent's failed measures as the new entry reads them, and what its repairs and the
ideas below them gave.

| | 7.d calls (failed measures: calls) | repairs tested | ideas below them | profitable | USD |
|---|---|---|---|---|---|
| night 9, kept | 31 (1: 13, 2: 18) | 37 | 55 | 14 | 135.1 |
| night 9, **skipped** | **16** (3: 7, 4: 7, 5: 2) | 29 | 11 | **0** | 54.5 |
| nights 7 to 9, kept | 85 (1: 48, 2: 37) | 84 | 98 | 18 | 274.7 |
| nights 7 to 9, **skipped** | **31** (3: 14, 4: 11, 5: 6) | 52 | 38 | **0** | 124.4 |

As expected: 0. (The review counted 51 repairs of far parents; this script finds 52, matching by lineage code.)

**Both: run_idea on one seeded idea** (`build_b11_b12/run_one.sh`, as `build_a4_join/run_one.sh`: plan, verdict and step
7 outputs copied, no model call; "old" runs the code of `7b7f0e8`). Idea 074-01.b1.g1 (night 9, confirmed and
profitable: neither rule changes it). `run_one_compare.txt`: 1,118 files each side; 431 identical, 676 identical once
times, ids, paths and durations are masked, 11 different, each named:
- the unseen-dates test (`unseen_test`) reruns step 5 on the dates no fold covers, and the new rule applies there too
  (one rule): 2026 period unclear -> no effect (t +0.019, 80 cases); 2016-2017 stays unclear, with the effect check
  line (t +1.196). Files: its 2 `result.json`, 2 `verdict.md`, 1 `INDEX.md`, the unseen json's `step5` field, its log
  line. "Holds" (main measure's sign and Sharpe) is the same in both: holds, holds;
- the order the step 7 lines are logged in (`journal.jsonl`, `table.json`, `table.md`) and one duration (6.5 against
  6.4 minutes): the lines run at the same time, as in build A4's proof;
- `trading-bot/results/trading_bot.log`: the order the coins were fetched.
The idea's own plan, record, verdict, check, chart files, register and step 7 files: identical.

**Tests**: the cards' tests 209 passed; the bot's tests (`cd trading-bot`) 1,682 passed, 16 skipped. `fold_rules_test.csv`
restored. The repository is clean after every proof run.

## What is not done, open
- The full rerun of 184 stored `measure.py` (21.8 hours of step 4): replaced by parts 1 and 2 above.
- Line 7.c's prompt changed (its first two lines: "no effect" in place of "clear evidence against it"); no model call
  was made with it.
- `run_viewer/runs.html` not rebuilt (it is a built page; `page.html` and `build_page.py` changed).
- Folder names kept: `07b_inconclusive/`, `07c_rejected/` (their runs are under them). A rename is a clean-up for the
  operator's go.
- `common/idea_definition.md` still says "if rejected, a reason to refuse one": it is pasted into steps 2 and 7's
  prompts, so changing it changes their requests. For the operator.
- Old records are not rewritten: an old unclear answer with t below 1 stays "inconclusive" where it is recorded
  (`select_next` reads only "confirmed"). An old "rejected" is read as "no effect" by 7.c's entry, `run_idea`'s row and
  the run viewer.
- `topics/NEXT_STEPS.md` lines B11, B12 not updated here (the designer's file). Merging is the operator's go.
