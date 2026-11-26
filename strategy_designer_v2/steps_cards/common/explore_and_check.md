What "exploring and checking on different years" is (the operator, 2026-11-24; topic 31). Read by step 7
(`07_common/helper/analyse.py`), step 5 (`05_verification/helper/make_verdict.py`) and the operator.

**An idea is chosen on some years and checked on others.** Step 7 looks at a backtest's results on the exploration
years before it writes an idea; step 5 judges the idea on every year, and a confirm must also point its way on the years
step 7 did not look at.

**Why.** Step 7 chooses a new idea after looking at a backtest's results (its explorations). Judged on the same years, the
chosen idea looks better than it is: a known effect of choosing on the data that judges. Judging on fewer years is not
the answer: with 4 of the 8 years, half the real effects are no longer confirmed (topic 31, measured on 125 books). But a
real effect keeps its direction on 4 years: on folds A and D alone, 122 of those 125 (98 %).

**The rule.**
- **The exploration folds: B and C** (2018 to 2021). **The check folds: A and D** (2022 to 2025). Each half holds a
  crash, a rising market and a choppy year.
- **Step 7 explores only the exploration folds** of the backtest it reads: its explorations see the windows of folds B
  and C; it is told that folds A and D are kept for the check. (It still reads the parent's verdict and size, measured on
  every fold: summaries of the parent idea, not of the ideas it will write.)
- **Step 5 judges on every fold** of the plan, as before; and when its verdict is "confirmed", it applies the same
  measure to the check folds alone: the **direction check**.
  - It **agrees** when the main measure there points the same way as on all the folds.
  - It **disagrees** when it points the other way: the verdict becomes "inconclusive" ("confirmed on every fold, the other
    way on the check folds").
  - It is **not judged** when the check folds hold too few cases (under 100 cases or under 30 days, the verdict's own
    minimum), when the plan has no check fold, when the measure cannot run on them alone, or when the backtest did not
    run on the plan's folds (an unseen-dates record): the verdict stands.
  - The cases are the measure's own: a strategy that trades only in its situation (its regime) is checked on the days of
    its situation in folds A and D only.
- One rule for every idea, written by step 2 or by step 7.

**What it costs.** About 2 real effects in 100 (measured above); on 64 confirmed verdicts rerun, 1 turned inconclusive
(`05_verification/card.md`, "Variants compared"). **What it does not do:** it does not stop the search
from finding the effects the portfolio already holds (they are real in every year); that is the order's job
(`orchestration/select_next/`, the held books).

**Why this cannot leak.** It removes data from step 7's view and adds a check on data step 5 already reads; no decision
reads a bar after its close.
