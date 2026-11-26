---
line: 7.d confirmed, not profitable
backtest: 031-01.g1_wide-day-low-close-rebounds_1d
idea tested: 031-01.g1_wide-day-low-close-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4376 USD
---
## Findings
- **F1:** The book fails on Calmar (0.694 against 0.75): its deepest fall is −16.4 % against a yearly return of +11.4 %, and this fall builds across w20 to w22 (window falls of −14.0 %, −16.1 % and −16.4 %). In those windows the 85 cases had a mean next-day return of −0.16 %, were held at a larger mean allocation (1.19 against 1.02 over all cases) and sat in calmer coins (mean coin-volatility quartile 1.14 against 1.45).
- **F2:** The idea's move depends on how volatile the coin has been. Split by each coin's own 20-day volatility quartile, the cases' excess next-day return rises from −0.21 % (t −0.53, 129 cases) to +0.52 % (t 1.44, 141), then +1.39 % (t 3.70, 130), then +3.78 % (t 4.52, 115).
- **F3:** The volatility condition alone does not earn. On days with no signal, the same quartiles give excess next-day returns of −0.08 %, −0.06 %, −0.08 % and +0.07 % (t 0.69 in the top quartile, about 3,500 days each). The rise belongs to the wide low-close day in a volatile coin, which fits the brief: a failed push only exhausts sellers when the push is large.
- **F4:** The volatility-target sizing puts most money where the effect is absent. The lowest-volatility cases carry the largest mean allocation (1.38) and the highest-volatility cases the smallest (0.72). By allocation quartile, the excess return falls from +3.16 % (t 4.66) in the smallest quarter to +0.15 % (t 0.42) in the largest. The 15 worst cases by P&L were held at 1.33 against 1.02 on average, and in calmer coins (volatility quartile 0.92 against 1.45).
- **F5:** A proxy of the same book with fees of 0.19 % per trade reproduces the record: Calmar 0.69, deepest fall −16.5 %, Sharpe 0.97.
- **F6:** Holding longer does not help. The second day after a case adds −0.26 % (t −1.04), so the rebound is spent in one day.
- **F7:** How far the drop is normalised changes the picture. Measured against the coin's own volatility, the drop does not grade the move (quartile means +1.56 %, +1.06 %, +0.56 %, +1.93 %), and large normalised drops without the signal earn −0.02 % (t −0.09, 566 days). Measured in raw percent, the largest drops give +2.96 % (t 4.16) against about +0.7 % to +1.2 % for the rest. The raw size of the move carries the effect, not its size relative to volatility.

## Ideas
- `031-01.g1.d1_rebound-grows-with-volatility` (from F2, F3, F4, F5): After a day whose high-low range is wide compared with its average daily range over the past 20 days and whose close lands near the day's low, the coin rises over the next 1 day, and this rise in percent is larger the higher the coin's daily volatility over the past 20 days is against its own usual level. The rise grows faster than that volatility, so the most volatile coins give the largest rebound per unit of risk.
- `031-01.g1.d2_wide-low-close-in-volatile-coins` (from F1, F2, F3, F5, F6): After a day whose high-low range is wide compared with its average daily range over the past 20 days and whose close lands near the day's low, only while the coin's 20-day daily volatility is high against its own usual level, the coin rises over the next 1 day. The wider that day's range against its 20-day average and the closer its close to the low, the larger the rise.
- `031-01.g1.d3_deeper-wide-day-fall-rebounds-more` (from F2, F7): After a day whose high-low range is wide compared with its average daily range over the past 20 days and whose close lands near the day's low, the coin rises over the next 1 day, more the larger that day's fall in percent.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
