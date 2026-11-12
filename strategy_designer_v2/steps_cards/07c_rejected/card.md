# Step card 7.c: Rejected (2026-11-12)

## Business objective
**Establish why an idea was rejected, what the market did instead and where, and propose another idea that could be confirmed.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 5's verdict is **rejected**: clear evidence against the idea. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
The direction and size of what happened instead; where it holds and where it does not (coins, periods, regimes, the size of the forecast, each side).

## What it proposes
Counter-ideas: the opposite effect, or the condition under which the idea fails or holds.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
No real idea is rejected yet. The planted record 002-05 with a planted fall (`05_verification/planted_test/`), rejected by step 5. Its prices were changed after the backtest, so its book does not match them: a test of the mechanism only.

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and the operator would test at least one of its ideas. Status: exercise 1 ran (`../07_common/exercise_1/reading.md`); not met yet (one exercise).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
