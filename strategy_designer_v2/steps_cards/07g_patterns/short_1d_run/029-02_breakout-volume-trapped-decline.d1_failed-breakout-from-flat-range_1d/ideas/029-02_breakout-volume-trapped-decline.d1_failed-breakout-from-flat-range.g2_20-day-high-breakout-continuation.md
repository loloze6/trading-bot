---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
line: 7.g patterns
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close sits above its highest close of the prior 20 days, measured in units of its 20-day volatility, the more the coin rises above its normal drift over the next 5 days.
Consequence: A trader would treat a fresh 20-day closing high as a reason to stay long, never as a setup to fade, and would hold more conviction the clearer the break.
Why:
- F5: A close above the prior 20-day high is followed by a positive 5-day unusual move in all three terciles of breakout size (+1.63 %, +1.18 %, +2.05 %; strength 0.12 to 0.16) and in both halves (t 1.25 and 1.80). The size of the breakout does not grade the move, so there is continuation and no reversal.
- F4: Failed breakouts carry no graded fall. Grouped by depth below the old high, the 5-day unusual move is +0.40 % (deep, t 0.39), +1.04 % (mid, t 0.79) and -0.64 % (shallow, t -0.44), with signs that disagree across coins (ZEC +3.50 %, BTC -0.91 %). The step-5 main t is -0.85 on 641 cases.
- F1: The pooled least-squares slope of the 5-day unusual move on the day's return in units of the coin's 20-day volatility is positive, at 0.00511 per unit, with t 2.66 on 2,699 non-overlapping cases; it is positive in all six coins (t from 0.10 for LTC to 2.37 for XRP), in both halves (w1-w12 t 2.57, w13-w24 t 1.40) and in 6 of 8 years.
