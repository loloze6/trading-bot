# Step card 7.g: Patterns (2026-11-12)

## Business objective
**Establish what patterns a backtest's bars and book show that the idea does not explain, and propose the ideas they suggest.**

The parts every line shares (input, output, how the data is read, the model, storage, quality criteria) are in `../07_common/card.md`.

## Entry condition
Every backtest (`helper/line.yaml`), **in a run, only when an idea it would write would be the next idea tested** (the
operator, 2026-11-27, next steps B10). When we want an idea from a discovery rather than keep the line of the idea
being tested: when the discovery would be the next idea tested.
- **The rule:** after a test, before the step 7 lines start, an idea this line would write gets select_next's own
  score: the higher of the records "7.g" (its follow-ups) and "7.g discovery" (a discovery's brief), over 1 plus the
  generation it would have (the tested idea's, as ranked, plus one). It is compared with the priority of the best
  waiting idea, as select_next ranks the queue (the loop's failed ideas left out). While a brief's own idea waits, it
  goes first: the line is not called. Otherwise the line is called when its score is at least that priority (ties
  included), or when nothing waits.
- **Why the score, not a priority with w:** w is the tested book's difference from the held books; what this line finds
  is a pattern that book does not explain (a discovery is off its theme), so the book's w says nothing about it. Tried
  and rejected (2026-11-27): the idea given the tested idea's w and group, compared by group then priority. On night 9's
  replay it skips 156 of 184 calls instead of 52, and 6 of the night's 11 profitable strategies have a skipped call on
  their path, against none with the rule (`../runs/BUILD_B10.md`).
- **Where:** in the one place `run_idea` calls the lines (`../orchestration/run_idea/helper/run_idea.py`,
  `call_patterns`; the score: `../orchestration/select_next/helper/select_next.py`, `discovery_call`). A call not made
  is one line in the run's journal, `not called:` and the two priorities compared; no analysis, no index line. An
  analysis already in the run is not decided again.
- **Why:** night 9, the line was called after each of 184 tests, 90 of 224 USD of model calls (40 %), and every run
  ended with 20 or more ideas never tested: 84 of 165 discovery briefs never tested. An idea that would not be tested
  next is paid for and waits. No budget, no number chosen: the rule is the ranking's own.
- **Rejected:** 7.g only after a confirmed test (it would have lost night 9's 10 profitable discoveries, all found after
  an unclear test); only when the queue is empty (it never emptied in night 9).
- **Proof:** night 9's six runs replayed (`../runs/BUILD_B10.md`).

## Input
The shared input: the backtest record, its plan and brief, step 5's verdict and step 6's check.

## Output
One analysis per backtest that meets the entry condition: findings, then ideas in step 2's format, or "no ideas" with the reason (`analyses/`).

## What it looks for
Angle by angle: the forecast (what follows small and large values), the positions, the trades, the regimes, and the bars (returns after large moves, by volatility level, by weekday and hour, by regime, around the book's largest gains and losses).

## What it proposes
New ideas, each from a finding, written like any idea. A pattern that cannot be told apart from chance is not a finding, and the more angles looked at, the more a pattern must stand out. If none does, "no ideas", with what was looked at.

The line is given the profile map (`../orchestration/ideas_similarities_check/register/PROFILE_MAP.md`,
`../common/market_profile.md`; the operator, 2026-11-25, next steps 1q): it looks first for discoveries in the market
profiles the map shows empty or thin, names the profile a pattern lives in, and does not write as a discovery an idea
the map already lists in the same profile. Why: on night 7, 29 of 70 discoveries were the next-day rebound after a fall,
already held, and 31 of the 51 confirmed books were that one effect.

**In a run with a target box** (`../common/target_box.md`; next steps B2.1, 2026-11-27): the box is part of the brief's
theme (`../07_common/card.md`, the note after the brief), and a discovery is looked for inside the box only; the map
then shows what the box already holds. Why: night 8's rising agitated session found 0 of 167 discoveries in its box;
the line followed the map to its other empty boxes.

Each idea is marked `theme: on` (on the brief's theme) or `theme: discovery` (off it; `../common/theme.md`). A
discovery is written as a source for a new brief (`discoveries/`), not as a follow-up; the loop turns it into a brief
of its own (operator, 2026-11-24; topic 50). Why: a pattern off the theme answers another question; tested as its own
theory's first idea, it is not counted as the old brief's result (night 6: "a week's gain carries into Saturday",
found from the yearly-low brief).

## The AI
The shared mechanism (`../07_common/helper/analyse.py`), with this line's `helper/line_prompt.md`. Opus.

## Fixed inputs for the iterations
The full-data run's 002-03 (daily, 6 coins, 8 years) and the hourly run's 001-01 (hourly, BTC and ETH, fold A).

## Variants compared
One call against analyst then deducer: one call kept, for every line (`../07_common/card.md`).

## Done when
On two exercises in a row, on the fixed inputs, every analysis meets the shared quality criteria and keeps to this line's objective, and at least one of its ideas, taken through steps 3 to 6, changes the result that sent the backtest to this line: one of its ideas is confirmed (operator, 2026-11-14). Status: **validated** (operator, 2026-11-15) by exercises 3 and 4 (`validation/reading.md`): its calm-coin idea confirmed (t 3.34); on the hourly input both runs answered "no ideas" for the same reason. Earlier: exercises 1 and 2 ran (`../07_common/validation/reading.md`).

## What this line does not do
It does not test its ideas, write a test plan, or look beyond its objective.
