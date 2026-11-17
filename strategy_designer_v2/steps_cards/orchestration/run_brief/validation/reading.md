# run_brief: validation on night_run (2026-11-17, in the operator's absence)

**Calls.** `run_brief.py BRIEF --run night_run --python VENV --budget B`: brief 003 with budget 6, then brief 011 with
budget 25 (the run's total), the second call made three times (twice resumed after a machine restart).

| Check (the card's "done when") | What happened |
|---|---|
| Step 2 writes the brief's ideas in the run | 003: 4 ideas (0.04 USD); 011: 6 ideas |
| The loop's first turn tests the idea `select_next` ranks first among them | 003-01, then 003-02 to 003-04; 011-01 |
| The loop goes on with the lines' ideas | from 011-01: 22 ideas of generations 1 to 3 (7.b, 7.d, 7.g) |
| It stops on the budget and says so | "budget reached (25.48 of 24.91 USD)": 24.91 is 25 less steps 1 and 2 (0.09 USD) |
| A second call makes no model call for steps 1 and 2 | step 2 "skipped: its output exists", three times |
| One run holds several briefs | 003 and 011 in one queue |

**Met.**

**Found and fixed on the way (general rules, tests added):**
- **A machine restart left an idea half-run.** Its plan existed, so `select_next` counted it as tested and it would
  never get its backtest and verdict. `loop` now finishes such an idea first when it resumes (`loop/card.md`).
- **An idea step 3 could not plan counted against its line's record.** A record now counts only ideas with a verdict.

**Not met by the function, by the data:** brief 003 could not be tested at all: no component measures volume against
its own average (parked for the operator).
