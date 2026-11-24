# Orchestration: the functions that chain the steps

The steps are used exactly as validated; an orchestration function only calls them in order and passes their files
from one to the next. One folder per function, named after it, with the same layout as a step: `card.md`, `helper/`,
`validation/reading.md` once validated, and its output for a named run in `<name>_run/`. A function card keeps the
step card's spine (objective, input, output, definition, storage, how to call it, done when) and replaces what only a
model step needs (prompt, model variants) with what a function needs (its turn, its rules, failures, state, visibility).

| Function | Card | Starts from | What it does | Status |
|---|---|---|---|---|
| `run_idea` | `run_idea/card.md` | one idea | steps 3 to 7, once, with its journal, logs and consumption | met on its fixed input (scope 1) |
| `loop` | `loop/card.md` | one idea | `run_idea`, then picks one of step 7's ideas and runs it again, until a stop rule | met on demo_run, budget 4 USD: 3 turns, stopped on the budget (scope 2) |
| `select_next` | `select_next/card.md` | a run | ranks the ideas written in the run (by step 2 or a step 7 line) and not yet tested, by one score: the record of the line that wrote it / (1 + its generation) | met on demo_run (called by `loop`) |
| `unseen_test` | `unseen_test/card.md` | an idea confirmed and profitable | its plan unchanged on every unseen period (steps 4, 5 with its own measure, 6); whether it holds (called by `run_idea` after step 7) | validated: `unseen_test/validation/reading.md` |
| `run_brief` | `run_brief/card.md` | a brief, a theme or a source | step 1 (theme or source only), step 2, then `loop` over one queue fed by step 2 and the step 7 lines | met on night_run (scope 3): `run_brief/validation/reading.md` |
| `ideas_similarities_check` | `ideas_similarities_check/card.md` | a paying book (step 5 confirmed, step 6 profitable enough) | keeps its returns in a register of paying books and compares it with every other one and with holding: its nearest relative, how much that book explains, who acts first, what is left (topic 41) | met (`validation/reading.md`); who reads it and whether `run_idea` calls it: open (topic 41) |
| `night_merge` | `night_merge/card.md` | the night's branches | merges them into the working branch by one rule per shared file (the components file class by class, the appended files line by line, the register by key, derived files rebuilt), checks nothing is lost or invented, runs both test suites (next steps 3g) | built 2026-11-24; proof: night 6 replayed |

The speed study (how long one idea's run takes and how to make it faster; topics 21 and 33) is a study, not a function:
its notes moved to `../topics/33_review/duration/` on 2026-11-21 (round 1: files 1 to 9; round 2: files 10 to 14).

## What the manual orchestration did that the next functions should keep (2026-11-15)
From the overnight run and the step 7 validation loops, run by hand:
- **Do not test an idea twice in a run** (same text, same data): lines proposed the same idea more than once. Kept: `select_next`.
- **Compare an idea's result with its parent's** (for example 002-03: Calmar 0.39 before the repair, 0.92 after): it
  is how a line was judged relevant. The row's `parent` field makes it possible. Not built: the table has both rows, not the comparison.
- **Stop rules:** kept in `loop` as: the operator, an optional budget, no candidate left (no default limit, operator 2026-11-16).
- **The order of the ideas to try**, not by step 7's own numbers (inflated by its search). Kept: `select_next`'s score.
- **A result produced by an earlier version of a step is stale** (the sizing rule made earlier backtests outdated).
  To design.
- **Test a confirmation or a profitable book on data the analysis never saw**: half the night's confirmations did not
  hold on other coins. Kept (2026-11-18): `unseen_test`, on dates no fold covers.
