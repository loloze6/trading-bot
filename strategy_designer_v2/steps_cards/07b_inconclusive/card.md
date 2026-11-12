# Step card 7.b: Inconclusive (2026-11-12)

## Business objective
**Establish why an idea's result is unclear although its test had enough cases, and propose ideas that would give a clear answer.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 5's verdict is **inconclusive**: enough cases, but neither the confirm nor the reject rule is met. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
The size of the effect and how much it varies; whether it is present in part of the data only (some coins, periods, regimes, the largest forecasts, one side); whether the market's own moves drown it.

## What it proposes
Ideas that state where the effect is, when the findings show it in part of the data: a condition, one side, the strongest cases.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
The full-data run's 002-01 and 002-03 (6 coins, folds A to D), both inconclusive.

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and the operator would test at least one of its ideas. Status: exercise 1 ran (`../07_common/exercise_1/reading.md`); not met yet (one exercise).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
