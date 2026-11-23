# Book reflects the idea, phase A (topic 47, item 1a; operator's go 2026-11-23)

## Purpose
Measure, before any build, what a book that trades the idea's situation (and nothing else) gives, against the book
step 3 built on night 5, for the ideas whose book had no situation gate (26 of the 72 real books that do not pay: in a
position on 98 % of the days, median, though most of their ideas name an event: "buys only the days whose volume surge
is several times usual", "fade only the largest moves").

## What is run
Five night-5 ideas (confirmed by step 5, not paying at step 6, no situation gate), each plan and config copied
unchanged but for one rule, the same for all five (no tuning per idea):
- **The situation is present when the idea's score is at least twice its usual size** (its mean absolute value over
  the standardise window): a `threshold_filter` at 20 placed right after the `standardise` step (which gives 10 x the
  score over its usual size, capped at 20). Otherwise the forecast is 0 and the book holds nothing.
- The side and the horizon stay as the plan set them (the idea's side; `min_holding_bars` = the idea's horizon).
Then steps 4 (backtest), 5 (the original verdict's `measure.py`, unchanged: no model call) and 6.

| # | Idea | Bar | Problem on night 5 |
|---|---|---|---|
| 1 | 030-03...d2_absorbed-selling-low-close | 1d | long only, fell with the market (2022) |
| 2 | 030-03...d1_extreme-surge-low-close-rise | 1d | long only, fell with the market |
| 3 | 030-03...g1_volatility-scaled-fall-next-day-rebound | 1d | trade does not pay its cost |
| 4 | 017-02...d3_four-hour-fade-of-extreme-hours | 1h | trade does not pay its cost |
| 5 | 017-05...b2_deep-two-hour-fall-rebound | 1h | long only, fell with the market |

Not in it: the two-sided ungated books (2 of 26): one is built from a score and a permanent short, which the rule
would change in kind.

## Expected outcomes (written before the run)
- E1. Days in a position fall a lot for all five (from 71-100 % to well under half).
- E2. Long-only books (1, 2, 5): the deepest fall shrinks; Calmar rises; whether it passes 0.75 is open.
- E3. Books whose trade did not pay its cost (3, 4): the edge per trade rises; whether it passes the round trip is open.
- E4. Step 5 still confirms most of them (the effect is the same, on fewer, larger cases); some may fall short of the
  measure's minimum number of cases and read inconclusive.
- E5 (the case against): if days in a position fall but the falls and the edges do not change, the loss is not the
  book's shape, and step 3 is not the step to develop.

## Reading (2026-11-23, about 18:40 Paris; `topics/47_review/phase_a_compare.py`, `phase_a_compare.csv`)
| Idea | Book | Step 5 | Days in a position | Yearly return | Deepest fall | Coins over that fall | Calmar |
|---|---|---|---|---|---|---|---|
| absorbed selling, low close (1d) | night 5 | confirmed | 98 % | 24.2 % | 48.1 % | -66 % | 0.50 |
| | phase A | confirmed (t 5.09) | 12 % | 13.7 % | 34.3 % | -66 % | 0.40 |
| extreme surge, low close (1d) | night 5 | confirmed | 97 % | 21.3 % | 41.7 % | -66 % | 0.51 |
| | phase A | inconclusive | 12 % | 13.7 % | 34.3 % | -66 % | 0.40 |
| volatility-scaled fall rebound (1d) | night 5 | confirmed | 48 % | 15.2 % | 30.2 % | -40 % | 0.50 |
| | phase A | inconclusive | 6 % | 2.8 % | 25.9 % | +187 % | 0.11 |
| deep 2-hour fall rebound (1h) | night 5 | confirmed | 99 % | 25.3 % | 67.1 % | -66 % | 0.38 |
| | phase A | inconclusive | 56 % | 6.6 % | 67.4 % | -72 % | 0.10 |
| four-hour fade of extreme hours (1h) | night 5 | confirmed | 99 % | -55.7 % | 99.8 % | +155 % | -0.56 |
| | phase A | confirmed (t 9.34) | 27 % | -46.0 % | 99.3 % | +155 % | -0.46 |

(The two absorption books give the same book once only their situation is traded: both ideas name the same days.)

- E1 (days in a position fall a lot): **yes**, 6 % to 56 % from 48 % to 99 %.
- E2 (long-only: the deepest fall shrinks, Calmar rises): **no**. The fall shrinks by 0 to 14 points; Calmar falls in all
  three, because the yearly return falls more than the fall. The situation days themselves fall in the crashes: the
  absorption book's worst fall is still in 2022, coins -66 %. Buying heavy-volume falls in a crash is the idea's own
  exposure, not the book's dilution.
- E3 (cost: the edge per trade rises): **mixed**. Volatility-scaled fall: from -0.41 % to +0.24 % per trade after
  costs, but 2.8 % a year. Four-hour fade: worse (-0.20 % to -0.40 %); the effect loses after costs either way.
- E4 (step 5 still confirms most): **no, 2 of 5**. Three read inconclusive on the idea's own situation: night 5's
  "confirmed" for them was a confirmation of the graded score on every day, not of the situation the idea names.
- E5 (the case against): **holds for paying**. Days in a position fell; falls and Calmar did not improve.
- Seen besides: the edge per unit of time in the market rises where the idea is real: yearly return / share of days in
  a position from 0.25 to 1.11 for absorption. The edge is in the situation days; so is the crash.

**Reading:** trading only the idea's situation does not make these books pay: their worst falls come from the
situation itself, in crash periods (the operator's case 1, "wrong by design in that state"). It does change what step
5 confirms: 3 of 5 confirmations were of a book that did not test the idea. So:
- step 3 fidelity matters for the truth of a verdict (an idea is confirmed only if its own situation is), not for
  profitability;
- the lever for paying is the market state the situation happens in (item 1d), and the first measure is direct: the
  situation days' returns inside crash periods against outside.

## Then: crash periods (2026-11-23, operator's go; topic 47, 1d-1)
The guess after phase A (the situation days fall in the crashes) is **wrong**. Inside crash periods (two definitions,
the coin's state known before the trade) the trades earn as much or more than outside, with the same swing. The worst
falls are what a small edge with a large swing gives by chance: on shuffled days, 63 to 95 % of the shuffles fall at
least as deep. For these ideas the edge per trade (about +0.5 % after costs) is small against each trade's swing
(about 6 %): Calmar stays low whatever the shape of the book or the market state.
