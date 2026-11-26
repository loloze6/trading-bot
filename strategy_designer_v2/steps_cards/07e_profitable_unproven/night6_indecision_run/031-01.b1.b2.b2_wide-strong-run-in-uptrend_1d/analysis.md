---
line: 7.e profitable but not proven
backtest: 031-01.b1.b2.b2_wide-strong-run-in-uptrend_1d
idea tested: 031-01.b1.b2.b2_wide-strong-run-in-uptrend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3991 USD
---
## Findings
- **F1:** The book earns on long holds, not on the plan's 3-day horizon: the 1,489 trades held 3.5 days or less lost a mean of −2.29 % net (sum −3,406 %), while the 821 trades held more than 6.5 days made a sum of +12,321 % (mean +10.3 % for 7 to 10 days, +21.5 % for 11 to 20 days, +16.2 % beyond 20 days); the median trade is −0.13 % and only 48.9 % of the 3,105 trades win.
- **F2:** The book's gain sits on a few days: its 20 best days carry 86 % of its summed daily return, and without them its mean daily return falls from 6.82 bp to 0.97 bp.
- **F3:** Most of the gain is timing, not the market's own rise, but it is uneven across coins: timing per bar is +13.1 bp for XRP, +6.8 for ETH, +5.2 for BTC, +5.1 for ZEC, +0.6 for LTC and −0.6 for XMR, against a market part of 1.3 to 3.4 bp.
- **F4:** The book's regime gives its edge over longer horizons, and it loses when it is rarely in it: on non-overlapping cases, the coin's excess return in the 'trending' regime minus outside it is +0.51 % over 3 days (t 2.02), and +1.73 % against −0.72 % over 10 days (t 2.57, 499 trending cases). The book lost in 2018 (−3.2 bp a bar) and 2022 (−7.9 bp, in a position only 23 % of the time).
- **F5:** A coin's 20-day return scaled by its volatility grades its excess return over the next 10 days: the slope is +0.99 % per unit (t 2.55, 1,403 non-overlapping cases), and over 5 days +0.46 % (t 2.44, 2,843 cases). The top quintile gains +2.38 % over 10 days while the other four quintiles lie between −0.23 % and −0.68 %.
- **F6:** Inside the regime (60-day and 5-day returns positive), the 5-day rise alone grades the next 3 days: the upper half minus the lower half is +1.66 % (t 3.80, 1,651 cases). Over 5 days it is +1.54 % (t 1.98).
- **F7:** The day's range multiple adds almost nothing. Inside the regime its rank correlation with the excess return is 0.061 over 3 days (p 0.08), 0.020 over 5 days and −0.051 over 10 days. Its upper half minus lower half is +0.08 % over 5 days (t 0.10). The tested idea's own size is only 0.020 of a usual move (+0.20 %, t 0.68, 825 days).

## Ideas
- `031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days` (from F1, F4, F5, F3): The larger a coin's 20-day return relative to its daily volatility over those 20 days, the more the coin rises over the next 10 days.
- `031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues` (from F6, F7, F4): While a coin's 60-day return is positive, the larger its 5-day rise, the more it rises over the next 3 days, whatever that day's range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
