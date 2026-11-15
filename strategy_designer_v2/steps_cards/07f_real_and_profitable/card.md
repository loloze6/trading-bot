# Step card 7.f: Real and profitable (2026-11-12)

**On hold (operator, 2026-11-15):** "proven and profitable, what next" is to be designed as a topic of its own (`../POTENTIAL_ADJUSTMENTS.md`); this line is not validated or used until then.

## Business objective
**Establish what could break a confirmed idea and its profitable book, and propose how to check it.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 5's verdict is **confirmed** and step 6's check is **profitable enough**. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
How concentrated the gain is (coins, periods, regimes, a few trades); whether it depends on one market state; how much of the gross gain the fees take.

## What it proposes
Ideas that state the conditions under which the effect should hold, so a test can check them, or the same idea on other data.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
No real idea is confirmed with a profitable book yet. The entry condition is tested on the full-data run's records (it must not run).

## Variants compared
One call against analyst then deducer: one call kept, for every line (`../07_common/card.md`).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: the idea of what could break the idea or its book is confirmed (operator, 2026-11-14). Status: exercises 1 and 2 ran (`../07_common/validation/reading.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
