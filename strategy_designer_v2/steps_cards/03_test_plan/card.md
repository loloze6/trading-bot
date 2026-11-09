# Step card 3: Test plan (draft 1, 2026-11-09)

## Business objective, one question
How will we know whether this idea is real?

## Input
One idea from step 2, with its brief.

## Output
One test plan per idea, or "untestable", with the reason.

## What a test plan is
**A test plan is the one way we will check an idea against the market data, fixed before we look: what we measure, against what, on which data, and which result would confirm the idea and which would reject it.**

- One test per idea.
- A regime (an on/off condition around a graded component) is used only when the idea itself is a condition. Otherwise the config uses graded tools only, so the position never jumps from none to some.
- The vessel is the strategy config: the test plan is expressed as a config the engine runs. The config's hard rules apply: every forecast is graded (no on/off), and `standardise` is the first transform of every component.
- An idea the config cannot express is "untestable", with the reason. That is a result, not a failure.

## What a forecast is
**The forecast is a number computed at each bar's close, for one coin, from the idea's indicators. It sets the position the idea calls for: the share of the portfolio held in that coin. Positive means long, negative means short, and the size grows with how strongly the indicators show the idea's situation. Zero means no position.**

- The chain: indicators → forecast → position. A change in the forecast changes the position: it opens, adds to, reduces or closes it.
- The price move times the position gives the portfolio's gain or loss on that bar. The portfolio's value rises when the position's side matches the price's direction.

## The parts of a test plan
1. **The idea**, its brief and the brief's header, copied by the script: what is being tested.
2. **The config**: the test itself, written in the engine's language.
3. **The criterion**: the result that confirms the idea, and the result that rejects it.
4. **The data**: the coin and the bar size, from the idea's header when it sets them; otherwise, to start simple, BTC/USDT, 1d bars, fold A. Written by the script, not chosen by the model; the model is told them, because the config's settings depend on the bar size. The config has no key for coins, bar size or periods: they belong to the run.
5. **The deviation**: what the config tests that differs from the idea (for example, "after X" becomes "while X, fading"), or "none".
- **Or "untestable"**, with the reason, in place of 2, 3 and 5.

Each part gets its three lines (for, used by, without it) when the fields are written.

## The AI: the passage on the test criterion (draft, to be verified by testing)
```
How an idea is tested here. The idea is turned into a forecast: a number computed at each
bar's close, for one coin, from the idea's indicators. The forecast sets the position the
idea calls for: the share of the portfolio held in that coin, long when positive, short when
negative, larger when the indicators show the idea's situation more strongly, zero when the
situation is absent. When the forecast changes, the position is opened, added to, reduced or
closed. On each bar, the portfolio gains when the position's side matches the price's
direction, and loses when it does not. The backtest records, bar by bar, the forecast, the
position, the price and the portfolio's value.

Your criterion. Ask: if this idea is true, where would it show in the forecast, in its
changes, or in the portfolio's value, and what would we see there if it is false? State the
one result that would confirm the idea and the result that would reject it. Fit it to the
idea: an idea about rare extreme situations shows in what follows the largest positions; an
idea about a steady relation shows in gains that grow with the size of the position. Judge
before costs, and against simply holding the coin, so that the market's own rise is not
credited to the idea.
```

## Storage and naming
```
03_test_plan/
  card.md                      this card
  helper/
    system_prompt.md           the helper's instructions
    make_test_plan.py          one closed-book call; refuses only a major deviation; saves the plan and its config
    reference/                 trimmed copies of the strategy config guide and the component catalogue, pasted into each call
  plans/
    NNN-KK_short-name.md       one test plan per idea, named after the idea
    NNN-KK_short-name_config.json   its config
  exercise_k/                  the comparison exercises
```
The plan's header holds the idea, its brief and the data. Its body holds `Forecast` (in plain words), the config's file name, `Confirm`, `Reject`, `Inconclusive` and `Deviation`, or `Untestable` with the reason.

## The AI
**Closed book**, as in steps 1 and 2: one call per idea. The idea, its brief, the data and the two trimmed references are pasted in. The references are trimmed copies of the originals in `strategy-research/docs/`: everything that does not help write a config was removed (pipeline stages, decision numbers, the block manifest, the block combiner, the campaign sizing block), and three passages were aligned with this card (regimes only when the idea is a condition; `standardise` sets the scale, never `vol_target`). They must be refreshed by hand when the originals change.

**Checks in code** (`make_test_plan.py`). It refuses only a major deviation:
- no readable config and no untestable line;
- a config without `regime_detector` or `strategies`;
- a class or param the catalogue does not list (the engine would ignore it silently);
- a missing confirm or reject;
- a field over 300 words.

Up to three attempts. The script also tells the model the data's windows (from the fold, no dates), and that warm-up bars are loaded before each window.

**Model.** Opus. In exercises 1 and 2, sonnet twice changed the idea's side and wrote "clearly" where a number was needed. **Cost.** About 0.26 USD per idea; the references are most of it.

**Prompt**: `helper/system_prompt.md`.

## Fixed inputs for the iterations
Seven ideas from step 2, exercise 3 (opus), with their briefs:

| Idea | Case |
|---|---|
| `001-01` RSI high, then reversal | testable; a rare extreme; a short side |
| `001-03` RSI high, then continuation | testable; the same situation, the other answer |
| `002-01` up-cross, then drift | testable; a steady relation; no coins in the header, so the default data |
| `002-05` cross-to-cross span | testable; a state |
| `003-01` low-volume up move reverts | a condition: a regime is allowed |
| `004-01` altcoins follow bitcoin | untestable: another coin |
| `005-01` bearish RSI divergence | no divergence component in the catalogue |

## Variants compared
Exercises 1 and 2: opus and sonnet, one call per idea. Exercise 2 added three prompt lines from exercise 1 (one horizon, an inconclusive line, no constant inside a regime); all three held.

Exercise 3: the plan in two calls (plan in words, then config), opus then opus or sonnet. It is more honest about what cannot be built, but the config differs from the plan in 5 of 5 cases, so the criterion no longer matches the test. It also costs more with opus. One call is kept (`exercise_3/reading.md`).

Exercise 4 (opus): six changes from the second review of exercise 2: the exact forecast first, the data's windows, what the record holds, one main measure, the evidence as a number, and a code check on names. All held. The divergence idea is now untestable, and the criteria fit the data. Telling the model the window size made it shorten the moving averages; one line on warm-up fixed it (`exercise_4/reading.md`).

Exercise 5 (opus): exercise 4 plus one line on settings (the single most common convention). No fault (`exercise_5/reading.md`).

## Quality criteria on the test plan
- Untestable when the idea needs another coin, other data, or an indicator the catalogue lacks, or when the config cannot come close to the forecast the idea needs. Never forced.
- The `Forecast` line says, in plain words, what the config computes.
- The config follows the hard rules: `standardise` first, every strategy component graded, a regime only when the idea is a condition, no constant inside a regime, long only when the brief says so.
- The same side as the idea; settings from the brief, else the single most common convention.
- One horizon in bars; one main measure and at most one supporting check; the evidence as a number; overlapping returns counted once; minimum counts that the data's windows can give.
- Confirm, reject and inconclusive cover every result.
- The deviation states every difference between the config and the idea.

## Who judges the output
The operator: "if this test confirms, would I believe the idea; if it rejects, would I drop it?". Code checks the shape and the names. Each exercise has a one-page reading against the criteria.

## Done when
On two exercises in a row, on the fixed inputs, every plan meets every criterion. Status: exercise 5 is the first with no fault.

## Open
- **For step 2:** 002-01 (after the cross) and 002-05 (from cross to cross) become the same forecast in this vessel; only their horizon and measure differ.
- **The default data** (BTC/USDT, 1d, fold A) gives about 36 independent 20-bar samples. Ideas about rare or slow situations will often come out inconclusive. The fold and the bar size are the operator's to set.
