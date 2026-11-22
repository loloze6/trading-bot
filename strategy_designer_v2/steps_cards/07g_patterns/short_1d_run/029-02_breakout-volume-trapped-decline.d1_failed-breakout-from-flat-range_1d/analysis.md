---
line: 7.g patterns
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
idea tested: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3999 USD
---
## Findings
- **F1:** The pooled least-squares slope of the 5-day unusual move on the day's return in units of the coin's 20-day volatility is positive, at 0.00511 per unit, with t 2.66 on 2,699 non-overlapping cases; it is positive in all six coins (t from 0.10 for LTC to 2.37 for XRP), in both halves (w1-w12 t 2.57, w13-w24 t 1.40) and in 6 of 8 years.
- **F2:** After a large up day the coin keeps rising more than its drift. With z between 1 and 2 the 5-day unusual move is +1.71 % (strength 0.144, t 2.38, 255 cases), and with z above 2 it is +2.59 % (strength 0.224, t 2.06, 110 cases). After z below -2 it is only +0.46 % (t 0.45), so the response climbs with the size of the up day.
- **F3:** The up-day continuation (z above 1) is positive in every coin and in both halves: BTC +0.90 %, ETH +0.81 %, LTC +0.76 %, XMR +1.39 %, XRP +5.18 % (t 2.10), ZEC +2.82 %; w1-w12 +1.43 % (t 1.80), w13-w24 +2.49 % (t 2.58).
- **F4:** Failed breakouts carry no graded fall. Grouped by depth below the old high, the 5-day unusual move is +0.40 % (deep, t 0.39), +1.04 % (mid, t 0.79) and -0.64 % (shallow, t -0.44), with signs that disagree across coins (ZEC +3.50 %, BTC -0.91 %). The step-5 main t is -0.85 on 641 cases.
- **F5:** A close above the prior 20-day high is followed by a positive 5-day unusual move in all three terciles of breakout size (+1.63 %, +1.18 %, +2.05 %; strength 0.12 to 0.16) and in both halves (t 1.25 and 1.80). The size of the breakout does not grade the move, so there is continuation and no reversal.
- **F6:** The book is a short bet on the market and nothing more. Its active days (23 % of days) correlate -0.77 with the coin's return and average -0.144 % a day. Its 30 best days come with the coin at -13.9 %, its 30 worst with the coin at +15.4 %. Its 1,091 trades of up to 5 days lose 3.10 % each on average after fees, against a 0.19 % cost.
- **F7:** Over the 20-day return the pooled slope of the 5-day unusual move is positive (0.0207, t 2.69, 2,843 cases), but it carries the opposite sign in BTC, LTC and XMR and rests on XRP (t 2.23) and ZEC (t 1.82). It is weaker than F1 and not held across coins.
- **F8:** Next-day returns by weekday reach t 3.76 (Friday bar, +0.31 %) and -2.70 (Wednesday, -0.30 %), but the effect has no grading, and among the many angles examined it does not stand far enough apart to build on.

## Ideas
- `029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range.g1_large-up-day-continuation` (from F1, F2, F3, F5): The larger a coin's one-day rise measured against its own 20-day daily volatility, the more the coin rises above its normal drift over the next 5 days.
- `029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range.g2_20-day-high-breakout-continuation` (from F5, F4, F1): The further a coin's daily close sits above its highest close of the prior 20 days, measured in units of its 20-day volatility, the more the coin rises above its normal drift over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
