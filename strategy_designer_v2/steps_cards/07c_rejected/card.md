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
Two things. What the market did instead: its direction and size, where it holds and where it does not (coins, periods, regimes, the size of the forecast, each side). And whether the test measured the idea elsewhere than where it shows: another horizon, comparison or side.

## What it proposes
Ideas that could be confirmed: what the market does instead (often the opposite effect), an idea of its own written like any idea; or the tested idea amended to the part of the data where it holds, written in full. "No ideas", with the finding, when nothing could be acted on (operator, 2026-11-15).

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
001-01 (after a high RSI extreme, price falls back) on the 6 default coins, folds A to D: rejected, the price rises instead (t 2.58), from 7.a's proposal (2026-11-15). The planted record 002-05 (`05_verification/planted_test/`), a test of the mechanism only.

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: the new idea is confirmed (operator, 2026-11-14). Status: **validated** (operator, 2026-11-15) by exercise 2 (`exercise_2/reading.md`): both its ideas confirmed and profitable. Earlier: exercises 1 and 2 ran (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
