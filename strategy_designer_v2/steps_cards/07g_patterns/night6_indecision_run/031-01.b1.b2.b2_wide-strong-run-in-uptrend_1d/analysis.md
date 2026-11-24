---
line: 7.g patterns
backtest: 031-01.b1.b2.b2_wide-strong-run-in-uptrend_1d
idea tested: 031-01.b1.b2.b2_wide-strong-run-in-uptrend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3886 USD
---
## Findings
- **F1:** A day that closed below its open with a high-low range far above its 20-day average range (top quintile of red days, range 2.17× average) is followed by a 3-day move +1.51 % above the coin's normal drift (t 2.29 with same-day cases pooled, 450 cases on 171 days), while the other four range quintiles of red days give -0.43 % to +0.07 %; on the 3-day grid, wide days with a red body gave +1.50 % (448 cases) against +0.34 % for wide green days (495 cases, t 0.60 in the top green quintile).
- **F2:** The rebound after wide red days does not depend on the 60-day trend, at +0.62 % when the 60-day return was negative (628 cases) and +0.90 % when it was positive (287 cases); it is positive in 6 of 8 years, with 2022 (-1.06 %) and 2024 (-0.28 %) the exceptions.
- **F3:** The next day's unusual return falls almost steadily with the day's own return in units of its 20-day volatility, from +0.53 % after the bottom decile (mean -1.8 standard deviations, t 1.94, 1450 cases on 512 days) through +0.27 % in decile 2 to -0.25 % in decile 8; the bottom-decile rebound is positive on all 6 coins (+0.24 % on BTC to +1.06 % on XMR) and in 7 of 8 years (only 2024 at -0.04 %).
- **F4:** The tested book's edge sits only at its strongest forecasts: on held grid bars, the top forecast quintile (mean forecast 19.9) gave +1.67 % unusual 3-day move (t 3.52, 499 cases) while the four lower quintiles gave -0.20 % to -0.43 %; forecasts above 15 gave +1.38 % (t 2.40 pooled, 583 cases on 298 days), but -3.1 % in both 2018 and 2022.
- **F5:** Over all grid bars, the 3-day unusual move rises with the 5-day return, from -0.56 % in its bottom quintile to +0.72 % in its top (t 2.42, 1087 cases), and the top range-multiple quintile gives +0.89 % (t 2.94, 943 cases); this is the continuation the tested idea already trades, not a new pattern.
- **F6:** The brief's own situation is not visible. On flat-bodied days the move against the 5-day run is +0.13 % to +0.27 % over 3 days in every range tercile (t at most 0.75, 524 cases each), no larger on wide days than on narrow ones.
- **F7:** By weekday, the next-day unusual return is positive after Thursday (+0.25 %, t 2.63) and Friday (+0.31 %, t 3.76) and negative after Monday (-0.24 %, t -2.53) and Wednesday (-0.30 %, t -2.70); Thursday and Friday beat Monday and Wednesday in 7 of 8 years. This is a calendar effect with no grading, so I write no idea from it.

## Ideas
- `031-01.b1.b2.b2.g1_wide-red-day-rebounds` (from F1, F2): The wider a coin's day's high-low range compared with its average daily range over the past 20 days, and the further that day closes below its open as a share of its range, the more the coin rises over the next 3 days.
- `031-01.b1.b2.b2.g2_volatility-scaled-one-day-reversal` (from F3): The larger a coin's fall over the past day, measured against its own daily volatility over the past 20 days, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
