---
line: 7.b inconclusive
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3912 USD
---
## Findings
- **F1:** The tested result is close to zero, not merely short of the bar. Over 5 days the short-side unusual move is +0.19 % (t 0.69, 1355 cases), a strength of 0.013 against the ~0.05 of real ideas. At this size, t 2 would need about 8 times as many cases, more than the 19 coins of folds A and D could supply. The total move is -0.40 % because the coin's drift runs against the short side (-0.59 %), so it is -2.1 times the 0.19 % cost of a trade.
- **F2:** The supporting check could never pass as built. The forecast is saturated at -20 on at least half of the cases (median -20, upper quartile -20 to -8.8), so the "larger half" above the median was empty (0 cases against 1355).
- **F3:** The cluster reading itself is not graded. By quartile of the raw cluster value, the 5-day unusual move is -0.01 %, -0.05 %, +0.58 % and +0.23 %, and the 10-day move on a 10-day grid is +1.62 %, +0.34 %, +1.18 % and +0.42 %. The Spearman correlation between cluster value and 10-day move is -0.018.
- **F4:** What little there is comes from the regime, not from the lows above the close. All below-50-day-average bars on the 5-day grid give +0.42 % (t 1.54, 1420 cases), about what the signals give. On the 10-day grid the same bars give +0.58 % (t 1.12, 713 cases).
- **F5:** The idea's horizon puts the measure in the wrong place. On the signal's own bar the coin has already fallen 1.37 % (short side, t 8.7, 1365 cases). Over the next 1 to 3 days it bounces (-0.18 % t -1.35, -0.21 % t -0.91). The fall shows only by 10 days: +0.97 % (t 2.36) on the 5-day grid, but +0.90 % with t 1.80 over 902 cases on a proper 10-day grid. It fades again by 20 days (+0.73 %, t 1.03).
- **F6:** The 10-day fall is concentrated in the early windows, so it is unstable across periods. It is +2.18 % (t 2.77, 296 cases) in w1-8, against +0.23 % (t 0.22) in w9-16 and +0.30 % (t 0.44) in w17-24. Across coins it is positive on 5 of 6 but reaches t 2 on none.
- **F7:** The effect shows clearly where the signal day was an up day, a retest of the broken lows from below. When the coin rose about 5.4 % on the signal bar (lowest quartile of the short-side bar move), the next 10 days fall 2.98 % more than usual (t 2.97, 212 cases). The other three quartiles give +0.06 %, -0.11 % and +0.22 % (all |t| < 0.2).
- **F8:** This retest effect belongs to the lows above the close, not to up days in a downtrend in general. Below-average bars with the same largest same-day rise give -0.09 % over 10 days (t -0.09, 179 cases). The retest cases' 2.98 % unusual move is about 15 times the 0.19 % cost of a trade, and still clears it after the coin's normal 10-day drift.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend.b1_rebound-into-broken-lows-fails` (from F5, F7, F8, F3, F4): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, after rising that day back toward them, it tends to fall over the next 10 days, only while the close is below its 50-day average price, and the larger that day's rise toward those past lows, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
