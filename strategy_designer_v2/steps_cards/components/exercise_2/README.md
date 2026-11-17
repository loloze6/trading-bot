# components, exercise 2: the automatic path (2026-11-17, written before the run)

**Purpose.** Test the path the operator asked for, on a real run: `loop`, with no candidate left, calls the components
step on its own; what it builds unblocks the run's ideas; `select_next` counts them again; `run_idea` calls step 3 again
for them; they are tested; the loop goes on.

**The run.** `night_rsi_run` (brief 010, RSI): its 8 ideas were all refused overnight as missing-components (how long,
or how often, RSI has stayed above or below its midline); its loop stopped "no candidate left". Its 8 wishes are open.
Call: `loop.py --run night_rsi_run --python VENV --budget 10` (the run's total; 0.31 USD spent before).

**Pre-registered outcomes.**
- **A.** `loop.jsonl` shows one `components` line before any new turn; the step answers the 8 wishes (one or two built,
  the others exists, by rule 1); its cost counts in the run's spend.
- **B.** The ideas whose wishes are all answered built or exists become candidates; step 3 is called again for each
  (its new plan replaces the refusal; the journal keeps both); the planned ones go through steps 4 to 7.
- **C.** Step 3 still refuses some: their new wishes are open; the loop calls the step again only after 10 turns or
  before stopping, never twice without a turn.
- **D.** The loop stops on the budget or for no candidate left, and says so.
- **E.** A defect of the automatic path: fixed if general, written here.

## Reading (15:00 to 15:20 UTC; stopped on the operator's go once the path was proven; 4.40 USD of 10)

**The automatic path works.**

| Stage | What happened |
|---|---|
| The loop finds no candidate (8 ideas refused overnight) | it calls the components step on its own: one `components` line in `loop.jsonl`, before any new turn |
| The step answers the 8 wishes (1.28 USD, 28 minutes) | 4 built (`RsiAboveMidlineShareComponent`, `RsiMidlineAgeComponent`, and a setting on each), 4 exists |
| `select_next` | the 8 ideas are candidates again (ranks 1 to 8 in the queue) |
| `run_idea` on 010-01 | step 3 called again (02:38 then 15:08 in its journal), its plan uses the new component and records the new catalogue version; steps 4 to 7 run: inconclusive (t +1.65), not profitable (Calmar only); step 7 proposes ideas |

Outcomes: **A** met; **B** met on 010-01 (and its child b1: inconclusive, t -0.30); **C** not reached; **D** the operator
stopped it; **E** one defect (below).

**Why it was stopped.** After 010-01, the score ranked 010-01's children (0.33, 0.23) above the 7 other unblocked ideas
(0.10): the rest of the budget would have bought variants of one idea, not a test of the path. This is the operator's
open topic on the ranking (a line that confirms gets ahead of new ideas). The 7 ideas stay unblocked in the queue; one
idea was stopped mid-run (`…g1_rsi-share-continuation-calm-markets`): the loop finishes it first when resumed.

**Defect, fixed:** the loop's line for the step's call showed the last line of the step's model-call log, not its
summary (it read stdout and stderr together). It now reads the summary on stdout.

**Findings for the operator:**
- **The same measure, two answers:** "the share of bars with RSI below its midline" came back exists (the share above,
  mirrored) for 010-02 and 010-05, but built as a setting (`side: below`) for 010-06. Each is valid; together they are
  not standard. A rule to add: a mirror of a measure (1 minus it, or its negation) is the same measure, exists.
- **A setting that changes nothing on real data:** `tie_side` on `RsiMidlineAgeComponent` decides where an RSI of exactly
  50 counts; on real data it likely never differs. A check to add: a new setting is kept only if its output differs from
  the defaults' on real data; otherwise the answer is exists.
- **Engine fix applied** (the operator's go): the engine's history holds at least what the forecast waits for.
