# Step card 7.c: No effect (2026-11-12; "rejected" became "no effect" 2026-11-27, B11)

## Business objective
**Establish why the effect is not in the data, what the market did instead and where, and propose another idea on the theme that could be confirmed.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Step 5's verdict is **no effect** (`../common/verdicts.md`; B11, operator 2026-11-27): enough cases (30), and the effect
near zero or pointing the other way (its t in the idea's direction below 1, or the plan's reject rule met: the old
"rejected", read today as "no effect"). Otherwise the line does not run, and its index line says so (`helper/line.yaml`).
An unclear result (inconclusive: a sign of the effect, t from 1) goes to 7.b. Why: the follow-ups of an unclear test
with t below 1 were confirmed 10 times in 72 (2 profitable), against 17 in 56 (7) from 1 to 2 (nights 7 to 9); a
clearer test of an absent effect pays rarely, the market's other behaviour on the theme is this line's question.
The folder keeps its name (`07c_rejected/`): its runs' files are under it.

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
Two things. What the market did instead: its direction and size, where it holds and where it does not (coins, periods, regimes, the size of the forecast, each side). And whether the test measured the idea elsewhere than where it shows: another horizon, comparison or side.

## What it proposes
Ideas that could be confirmed: what the market does instead in the theme's situation (often the opposite effect), written like any idea; or the tested idea amended to the part of the data where it holds, written in full (operator, 2026-11-15). Every idea stays on the brief's theme (`../common/theme.md`; operator, 2026-11-24, topic 50): when nothing on the theme could be acted on, "no ideas: the theme's effect is not in the data", with the finding.

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
001-01 (after a high RSI extreme, price falls back) on the 6 default coins, folds A to D: rejected, the price rises instead (t 2.58), from 7.a's proposal (2026-11-15), in the validation run (`validation_run/` of steps 3 to 6). The planted record 002-05 (`05_verification/planted_test/`), a test of the mechanism only.

## Variants compared
One call against analyst then deducer: one call kept, for every line (`../07_common/card.md`).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: the new idea is confirmed (operator, 2026-11-14). Status: **validated** (operator, 2026-11-15) by exercise 2 (`validation/reading.md`): both its ideas confirmed and profitable. Earlier: exercises 1 and 2 ran (`../07_common/validation/reading.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
