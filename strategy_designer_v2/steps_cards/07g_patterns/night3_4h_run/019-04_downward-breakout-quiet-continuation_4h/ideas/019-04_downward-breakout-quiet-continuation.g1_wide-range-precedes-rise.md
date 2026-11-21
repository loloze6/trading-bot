---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's last two days of four-hour price range compared with its 30-day average four-hour bar range, the more the coin rises over the next three days.
Consequence: A trader leans long after a coin's recent two-day range has widened against its usual range, and refuses longs after an unusually narrow two-day stretch.
Why:
- F1: Over the next 18 bars (three days), a coin's return rises with the width of its past two-day range against its 30-day mean 4h bar range. On the offset-0 grid the narrowest fifth has an unusual move of -0.75 % (strength -0.085, t -2.83, about 1,030 cases) and the widest fifth +0.39 % (strength +0.044). The widest-minus-narrowest Welch t is 2.82, and it stays positive on all six grid offsets (t 1.12, 2.64, 2.60, 2.82, 3.70, 4.49).
- F2: The F1 relation holds on every coin, with per-coin Spearman rho from 0.039 (ETH) to 0.082 (XRP), all positive. It holds in 7 of 8 years, rho -0.002 to +0.156.
- F3: The F1 edge is large against the cost of a trade. The widest fifth's total move is +0.80 % per three-day case and its unusual move +0.39 %, about 4.2 and 2.1 times the backtest's 0.19 % round trip. The narrowest fifth's total move is -0.34 %.
- F4: The brief's premise is not seen: narrow stretches are not followed by larger moves. The mean absolute three-day move, in units of the coin's usual move, is 0.71 in the narrowest width fifth against 0.77 in the widest, with the middle fifths at 0.64 to 0.70.
