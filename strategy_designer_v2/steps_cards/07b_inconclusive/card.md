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
Two things. Whether the effect is weak or mixed: its size and how much it varies, whether it is present in part of the data only (some coins, periods, regimes, the largest forecasts, one side), whether the market's own moves drown it. Or whether the test measured the idea elsewhere than where it shows: another horizon, comparison or side. Or whether the result is on the idea's side but too small for this data.

## What it proposes
The answer step 5's result calls for (its main measure and statistic, not a measure of the line's own; operator, 2026-11-15):
- the result is on the idea's side but short of the bar, and more data is available than the test used: the tested idea unchanged, on more data: a `same-idea-on:` block (the line gives the data, from `../common/data_available.md`; code copies the idea's text); narrowing would leave fewer cases when the problem is too few;
- the result is on the other side or zero, or no more data is available: the tested idea amended to the part of the data where the findings show the effect clearly, written in full; or, if there is none, "no ideas", with that finding: a clear answer.

An idea of its own is written like any idea, without a label.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
The full-data run's 002-01 (a weak result, t 0.37), 002-03 (close to a confirm, t 1.73) and 002-04 (an effect that looks absent, t -0.23), all inconclusive, backtested with the current steps (6 coins, folds A to D).

## Variants compared
One call against analyst then deducer, on the fixed inputs (exercise 1).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: the new idea gets a clear answer (confirmed or rejected) (operator, 2026-11-14). Status: **validated** (operator, 2026-11-15) by exercises 3 to 5 (`exercise_5/reading.md`): its "more data" idea on 002-03 was confirmed. Its route (narrower idea, more data, no ideas) varies from run to run. Earlier: exercises 1 and 2 ran (`../07_common/exercise_2/reading.md`); used in the overnight run (`overnight_run/` in this folder, `../OVERNIGHT_RUN.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
