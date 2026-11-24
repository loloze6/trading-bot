---
line: 7.d confirmed, not profitable
backtest: 031-02.b1.g2.b3_next-day-rebound-after-falls_1d
idea tested: 031-02.b1.g2.b3_next-day-rebound-after-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3696 USD
---
## Findings
- **F1:** The book failed only on Calmar (0.72 against 0.75): its deepest fall was -27.6% over 119 days, from w8 into w9, while holding the coins fell 40.2% over the same stretch; w9 was the worst window for both the book (mean -0.141% a day) and holding (-0.256% a day).
- **F2:** On signal bars, the next-day rebound grows with how volatile the coin's past 10 days were against its past 60 days. By quartile of that ratio, the excess return was -0.18% (t -1.6) in the lowest, -0.01%, then +0.31% (t 2.9), and +0.58% (t 4.3) in the highest, with about 1,788 bars each.
- **F3:** The volatility condition does not earn on its own. On bars without a fall, the highest quartile of the 10-to-60-day volatility ratio had an excess of -0.42% (t -3.3), and ratios above 0.9 gave -0.28% over 3,639 bars. The rebound in high recent volatility belongs to the fall itself: the crowding theory's stretched one-sided flow, which is largest when recent moves are large.
- **F4:** The two measures combine. The deepest third of falls in the highest third of the volatility ratio had an excess of +0.87% (t 5.1, n 1,111), which is 4.6 times the 0.19% cost of a trade. Deep falls in the lowest volatility third had -0.14% (t -0.6), and shallow falls earned nothing in any volatility third (-0.14% to +0.08%).
- **F5:** An approximate book with costs, taking only falls with a volatility ratio above 0.9, kept most of the gain and raised Calmar above the bar: yearly return 19.4% against 20.1%, deepest fall -18.6% against -27.6%, Calmar 1.04 against 0.73, Sharpe 0.98 against 0.79, while in the market 20% of bars against 49%.
- **F6:** Keeping only the deeper falls does not repair the falls. Falls deeper than 0.66 standard deviations gave a Calmar of 0.65, and deeper than 1.1 gave 0.54. Deep-fall bars carry the largest positions (mean 0.88) and the fattest losses (5th percentile gain -6.1%), so depth alone concentrates the risk.
- **F7:** On signal bars, the rebound is U-shaped in the coin's 20-day return. It was +0.35% (t 2.4) after the largest 20-day falls and +0.45% (t 3.8) after the largest 20-day rises, against about 0 in the middle two quartiles. Without a fall, the largest 20-day falls were followed by -0.43% (t -3.5), so a large 20-day move alone does not carry a rebound.

## Ideas
- `031-02.b1.g2.b3.d1_dip-rebound-in-turbulence` (from F1, F2, F3, F4, F5, F6): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next 1 day. The rise is larger the more volatile the coin's past 10 days have been against its past 60 days.
- `031-02.b1.g2.b3.d2_dip-rebound-after-stretched-month` (from F7, F1): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next 1 day. The rise is larger the further the coin's 20-day return lies from zero.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
