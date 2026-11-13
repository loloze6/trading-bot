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
**First, what failed.** The check names the measures that failed; the analysis must explain those.
- The falls failed (Calmar, or one window carrying the result): the book's deepest falls, what the coin's bars showed before and during them, what the book held then. The question: when should this book not be in the market?
- The gain failed (Sharpe, gain against holding, mean return): where the gain is lost: the forecast's size against what follows, the trades against their fees, the market states that lose.
- It trades too little: what makes the signal rare.

Then the rest, only as far as it explains what failed.

## What it proposes
Ideas that change what failed. An idea that adds gain but leaves the failing measure where it is does not answer.
- A way of trading can become an idea about the market: a stop that would have saved the book says that after a given fall the coin keeps falling; a signal that trades too often says its information is in its slow part.
- A repair is the tested idea amended, written in full ("..., only while ...", "..., except when ..."). A separate claim would be tested alone and cannot repair this book.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
The full-data run's 002-01 and 002-03, both not profitable enough.

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and the operator would test at least one of its ideas. Status: exercises 1 and 2 ran; "start from what failed" approved by the operator on 2026-11-13 after the overnight test (`overnight_run/test_failing_measure/`) (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
