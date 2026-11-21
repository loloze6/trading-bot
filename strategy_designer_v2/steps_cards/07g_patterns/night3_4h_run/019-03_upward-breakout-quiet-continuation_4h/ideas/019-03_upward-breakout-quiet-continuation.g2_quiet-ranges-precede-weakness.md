---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The narrower a coin's last 2-day price range is compared with its 30-day average 4-hour range, the further its return over the next 3 days falls below its normal drift.
Consequence: A trader refuses long bets placed out of very quiet ranges and treats deep quiet as a reason to stay out.
Why:
- F5: Against the brief, the narrowest two-day stretches are followed by underperformance, not by a large move up. The quintile where the 30-day mean 4h range is largest against the 2-day range is followed by -0.101 of the usual move, -0.88 % (t -3.22, 1030 cases). The widest-stretch quintile gives +0.063 (t 1.75).
- F6: Upward breaks above the prior 2-day high add nothing on the grid: +0.048 (t 0.83, 385 cases), with no order across narrowness terciles (-0.007, +0.118, +0.004). This matches the inconclusive verdict, whose strength was 0.023.
