---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's volatility over its last 7 days compared with its volatility over its last 30 days, the more the coin rises over the next three days.
Consequence: A trader leans long into a coin whose short-term volatility is expanding against its monthly level, and stays out of longs while volatility is contracting.
Why:
- F5: Rising volatility is followed by higher returns, measured as 7-day hourly-return volatility over 30-day volatility. The highest fifth has an unusual 18-bar move of +0.70 % against -0.54 % for the lowest. The Welch t is 2.0 to 3.4 across all six grid offsets, and 5 of 6 coins have positive rho. By year it is weak, positive in only 5 of 8, so it overlaps F1 and is less stable.
- F1: Over the next 18 bars (three days), a coin's return rises with the width of its past two-day range against its 30-day mean 4h bar range. On the offset-0 grid the narrowest fifth has an unusual move of -0.75 % (strength -0.085, t -2.83, about 1,030 cases) and the widest fifth +0.39 % (strength +0.044). The widest-minus-narrowest Welch t is 2.82, and it stays positive on all six grid offsets (t 1.12, 2.64, 2.60, 2.82, 3.70, 4.49).
- F3: The F1 edge is large against the cost of a trade. The widest fifth's total move is +0.80 % per three-day case and its unusual move +0.39 %, about 4.2 and 2.1 times the backtest's 0.19 % round trip. The narrowest fifth's total move is -0.34 %.
