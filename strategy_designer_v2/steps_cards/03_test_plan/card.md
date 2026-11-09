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

The sections that follow the template (fields, storage, the AI, criteria, tests) are written once the test criteria are settled.
