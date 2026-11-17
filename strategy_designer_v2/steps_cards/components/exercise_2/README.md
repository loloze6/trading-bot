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

## Reading
(written after the run)
