# Run brief: the overnight run (2026-11-12 to 13)

**Purpose (operator, 2026-11-12).** Act as a manual orchestrator of the workflow: step 7's analyses on existing backtests; their ideas through step 3 (test plan), step 4 (backtest), step 5 (is the idea real?) and step 6 (is the book profitable?); step 7 again on the new backtests, the line chosen by steps 5 and 6; and again. Aim: an idea proven real with a profitable book. On the way, find improvements, test them (behind an option or clearly marked, the agreed default unchanged), and list them for the operator's review in the morning. Also settle step 7's mode: one call, or analyst then deducer.

## How the loop runs
- **Step 7:** every line whose entry condition holds. Generation 1 starts from the full-data run's backtests (brief 002, 6 coins, folds A to D, daily). 002-05 and 002-06 are skipped: their books are identical to 002-01 and 002-02.
- **Selection (the orchestrator's choice, logged):** at most about eight ideas per generation, chosen by:
  1. a one-coin config could test it;
  2. its findings carry strong numbers (a t of 3 or more, or the same sign on most coins);
  3. it recurs across lines or modes;
  4. it is distinct from the others and from ideas already tested.
- **Hand-off to step 3:** a clean copy of each chosen idea (its brief, its data lines, the idea and its consequence), without step 7's "Why", whose numbers come from the data. Step 3 stays closed book.
- **Data:** the default (6 coins, folds A to D, daily). An idea step 7 found in that data and then confirmed on it is circular evidence. So every idea that passes step 5 or step 6 is tested again on **unseen coins**: coins the analyst never saw, in folds A and D (the years where they have data). The holdout is not touched.

## Pre-registered outcomes
- **A.** An idea is confirmed with a profitable book on the default data, and holds on unseen coins: a candidate for the operator (the holdout is the operator's decision).
- **B.** Ideas pass on the default data but not on unseen coins: what step 7 finds in data does not carry over. The data rule for step 7's ideas becomes the first improvement.
- **C.** Nothing passes after the generations the night allows: the improvements list says where the workflow is limited.
- **D.** Defects found on the way: each goes to the improvements list.

## Where the outputs go
Each step's outputs in its own folder, under `overnight_run/` (`03_test_plan/overnight_run/plans/`, `04_backtest/overnight_run/backtests/`, and so on; step 7's in each line's folder). The orchestrator's own files (selections, hand-off ideas, the improvements log) in `overnight_run/` next to this brief.

## Result
To be written in the morning.
