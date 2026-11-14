# Step card 7.a: Not observable (2026-11-12)

## Business objective
**Establish why an idea could not be observed in its backtest, and propose how it could be made observable, without changing the idea.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 5's verdict is **not observable**: the test found fewer cases than its plan's minimum. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
How often the idea's situation occurs (per coin, per window, per year); how the forecast is spread; how many cases the plan asked for and got; how much the outcome varies.

## What it proposes
The same idea where it can be observed: on other data (other coins, another bar size, another period, in the idea's data lines), or stated at the time scale where its situation occurs often enough. Never a loosened situation, which would be another idea.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
Two real records cut to one window of one coin (`05_verification/exercise_11/records/`): 001-01 and 002-05, both not observable. Not market evidence.

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and the operator would test at least one of its ideas. Status: exercises 1 and 2 ran (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
