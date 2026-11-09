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
4. **The deviation**: what the config tests that differs from the idea (for example, "after X" becomes "while X, fading"), or "none".
- **Or "untestable"**, with the reason, in place of 2 to 4.

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

The other sections of the template (storage, the rest of the AI, criteria, tests) come next.
