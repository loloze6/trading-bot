---
line: 7.g patterns
backtest: 031-01.g1.b1_down-day-rebound-more-coins_1d
idea tested: 031-01.g1.b1_down-day-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6213 USD
---
## Findings
- **F1:** On down days, the day's high-low range measured against the coin's 60-day average range predicts the 3-day move above drift. The slope of the 3-day strength on the log scaled range is +0.196 (t 3.23, day-clustered, 4746 non-overlapping cases on 680 days). On up days it is −0.052 (t −0.96, 5147 cases on 697 days), so the effect sits on the down side only.
- **F2:** The effect is graded across down-day range quintiles. The mean unusual 3-day move runs −0.55 %, −0.45 %, −0.19 %, +0.46 % and +1.97 %. The top quintile has a strength of 0.22 and t 2.42 on 228 days, so its unusual move is about 9 times the 0.22 % cost of a trade.
- **F3:** The range carries the rebound, not the size of the fall. With both in one regression on down days, the log scaled range has a coefficient of +0.315 (t 4.15) and the scaled fall −0.129 (t −1.94). The tested scaled fall on its own has a slope of −0.022 (t −0.82), and its verdict size is +0.02 % (t 0.10).
- **F4:** What matters inside the range is how far the close sits above the day's low. Measured in the coin's 60-day average range, this lower-wick distance has a coefficient of +0.242 (t 3.17) on down days. Alongside it, the range falls to +0.089 (t 1.37).
- **F5:** Volume shows the same thing but adds nothing beyond the range. The log scaled volume slope on down days is +0.139 (t 3.21), and with range and fall included it drops to +0.031 (t 0.68).
- **F6:** The down-day range effect is broad and lasting:
- **F7:** Several other angles showed nothing that survives the number of angles looked at:

## Ideas
- `031-01.g1.b1.g1_down-day-lower-wick-rebound` (from F4, F1, F3, F6): On a day a coin closes down, the further its close has recovered above the day's low, measured in the coin's average daily high-low range over the past 60 days, the more the coin rises above its normal drift over the next 3 days.
- `031-01.g1.b1.g2_wide-range-down-day-rebound` (from F1, F2, F3, F5, F6): On a day a coin closes down, the wider that day's high-low range against the coin's average daily range over the past 60 days, the more the coin rises above its normal drift over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
