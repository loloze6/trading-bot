# Step card 7.d: Not profitable (2026-11-12)

## Business objective
**Establish why a backtest's book does not pay, angle by angle, and propose ideas about the market that would remove the cause.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 6's check is **not profitable enough**. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
Angle by angle: the forecast (the gain before fees; whether a larger forecast earns more); the trades (how many, how long, the gain before fees against the fees); the position and the regime (where the losses come from: regimes, periods, side, a rising or falling, calm or volatile market).

## What it proposes
Ideas about what the forecast should capture to remove the cause (for example: a signal that trades too often may hold its information in its slow part; losses in one market state may mean the effect holds only in another; a losing side may mean the effect is one-sided).

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
The full-data run's 002-01 and 002-03, both not profitable enough.

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and the operator would test at least one of its ideas. Status: exercises 1 and 2 ran (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
