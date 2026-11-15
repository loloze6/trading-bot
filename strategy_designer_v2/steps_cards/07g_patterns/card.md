# Step card 7.g: Patterns (2026-11-12)

## Business objective
**Establish what patterns a backtest's bars and book show that the idea does not explain, and propose the ideas they suggest.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
None: every backtest. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
Angle by angle: the forecast (what follows small and large values), the positions, the trades, the regimes, and the bars (returns after large moves, by volatility level, by weekday and hour, by regime, around the book's largest gains and losses).

## What it proposes
New ideas, each from a finding, written like any idea. A pattern that cannot be told apart from chance is not a finding, and the more angles looked at, the more a pattern must stand out. If none does, "no ideas", with what was looked at.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
The full-data run's 002-03 (daily, 6 coins, 8 years) and the hourly run's 001-01 (hourly, BTC and ETH, fold A).

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: one of its ideas is confirmed (operator, 2026-11-14). Status: exercises 1 and 2 ran (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
