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
Whether the gain is the market's own rise, one coin, one period or a few trades; whether it was earned in the idea's situation or elsewhere; in which market states.

## What it proposes
The idea the book actually captures, when the findings show one.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
No real book is profitable enough yet. The entry condition is tested on the full-data run's records (it must not run).

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and the operator would test at least one of its ideas. Status: exercises 1 and 2 ran (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
