---
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation_4h
idea tested: 019-04_downward-breakout-quiet-continuation
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4207 USD
---
## Findings
- **F1:** Over the next 18 bars (three days), a coin's return rises with the width of its past two-day range against its 30-day mean 4h bar range. On the offset-0 grid the narrowest fifth has an unusual move of -0.75 % (strength -0.085, t -2.83, about 1,030 cases) and the widest fifth +0.39 % (strength +0.044). The widest-minus-narrowest Welch t is 2.82, and it stays positive on all six grid offsets (t 1.12, 2.64, 2.60, 2.82, 3.70, 4.49).
- **F2:** The F1 relation holds on every coin, with per-coin Spearman rho from 0.039 (ETH) to 0.082 (XRP), all positive. It holds in 7 of 8 years, rho -0.002 to +0.156.
- **F3:** The F1 edge is large against the cost of a trade. The widest fifth's total move is +0.80 % per three-day case and its unusual move +0.39 %, about 4.2 and 2.1 times the backtest's 0.19 % round trip. The narrowest fifth's total move is -0.34 %.
- **F4:** The brief's premise is not seen: narrow stretches are not followed by larger moves. The mean absolute three-day move, in units of the coin's usual move, is 0.71 in the narrowest width fifth against 0.77 in the widest, with the middle fifths at 0.64 to 0.70.
- **F5:** Rising volatility is followed by higher returns, measured as 7-day hourly-return volatility over 30-day volatility. The highest fifth has an unusual 18-bar move of +0.70 % against -0.54 % for the lowest. The Welch t is 2.0 to 3.4 across all six grid offsets, and 5 of 6 coins have positive rho. By year it is weak, positive in only 5 of 8, so it overlaps F1 and is less stable.
- **F6:** The book is mostly an exposure against the coin's rise rather than timing. Its daily returns correlate -0.74 with the coins' daily returns, and every coin's book loses, by -0.008 % to -0.026 % a day.
- **F7:** Two patterns did not hold and give no idea:

## Ideas
- `019-04_downward-breakout-quiet-continuation.g1_wide-range-precedes-rise` (from F1, F2, F3, F4): The wider a coin's last two days of four-hour price range compared with its 30-day average four-hour bar range, the more the coin rises over the next three days.
- `019-04_downward-breakout-quiet-continuation.g2_volatility-expansion-precedes-rise` (from F5, F1, F3): The higher a coin's volatility over its last 7 days compared with its volatility over its last 30 days, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
