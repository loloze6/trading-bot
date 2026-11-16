# Step card 7.e: Profitable but not proven (2026-11-12)

## Business objective
**Establish what a profitable book really earns from when the idea behind it was not shown real, and propose the idea it captures.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 6's check is **profitable enough** and step 5's verdict is **not confirmed**. Otherwise the line does not run, and its index line says so (`helper/line.yaml`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
Two things. Whether the gain comes from something else than the idea: the market's own rise (as `../common/measures.md` defines it), one coin, one period or a few trades, another situation, which market states. Or whether it comes from the idea, but the test did not measure it where the book earns it: another horizon, comparison or side.

## What it proposes
The idea the book actually captures, when the findings show one.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
Two books profitable enough whose idea was not confirmed, backtested with the current steps: the 002-03 repair from 7.d (`002-03_...d1_above-average-drift-near-highs_1d`) and N2-04 (slow and fast momentum), in the validation run (`validation_run/` of steps 3 to 6). One book where the line must not run: N2-06 (not profitable enough, by a hair).

## Variants compared
One call against analyst then deducer: one call kept, for every line (`../07_common/card.md`).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: the idea of what the book earns from is confirmed (operator, 2026-11-14). Status: **validated** (operator, 2026-11-14) by exercise 2 (`validation/reading.md`): on both inputs the idea it proposed was confirmed and its book profitable. Earlier: exercise 1 and the shared exercise 2 ran (`../07_common/validation/reading.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
