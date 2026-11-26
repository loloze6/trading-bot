---
line: 7.g patterns
backtest: 032-02.g1_uptrend-near-high-continues_1d
idea tested: 032-02.g1_uptrend-near-high-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5594 USD
---
## Findings
- **F1:** Among grid cases in a 28-day decline, the nearer the close was to its highest close of the past 56 days, the lower the 5-day excess return that followed: slope -0.108, t -2.96 over 459 cases. All six coins point the same way (BTC t -2.46, LTC t -2.06, XMR t -1.85, ETH t -1.02, XRP t -0.74, ZEC t -0.52), 7 of 11 windows are negative, and at 2 days the slope is still t -2.01. In 28-day rises the same measure has the opposite sign (slope +0.123, t +2.43).
- **F2:** Among 28-day declines whose daily ranges over the 28 days were wide (at or above the median of 28-day mean range over 90-day mean range), a deeper 28-day fall was followed by a larger 5-day rebound: slope -0.140, t -2.85 over 277 cases. All six coins are negative (t -0.99 to -1.65) and 7 of 8 computable windows are negative. The deepest quartile (mean fall -45 %) gained +3.71 % excess (t 1.68), while the shallower three quartiles lost 1.4 % to 2.5 %.
- **F3:** In calm 28-day declines (narrow ranges), the slope of the 5-day excess return on the 28-day return is +0.107, t 1.90 over 277 cases, which is the brief's sign. It is not graded: by quartile from deepest fall to shallowest, the means are -1.58 % (t -1.13), -4.64 % (t -3.84), +0.72 % and +2.08 %.
- **F4:** Among 28-day rises, the closing-high proximity predicts the 2-day excess return more surely than the tested 5-day one: slope +0.133, t 3.47 over 638 cases, against step 5's t 1.65. Over all regimes, the top tenth of proximity (mean 0.9996) gained +4.23 % over 5 days (t 3.06), while tenths 2 to 4 (proximity 0.76 to 0.86) lost 1.9 % to 3.9 % (t -1.90 to -3.96).
- **F5:** The book's gain sits in its tails: its best 5 % of days carry 209 % of its summed daily gain, at +4.91 % against +7.08 % for holding on those days. On its worst 5 % of days it loses 4.05 % against 7.43 % for holding.
- **F6:** Trades entered at the lowest forecast quartile (mean forecast 6.9) earned +10.1 % after fees, against +4.4 % to +5.6 % for quartiles near forecast 15.7 to 20. Those trades lasted about 17 days against about 10 days, so holding length may account for the difference.
- **F7:** Weekday, 20-day volatility, the 5-day range ratio and the volume ratio showed no graded 5-day effect (slopes t -0.85 to 0.52) over about 30 angles explored, so only patterns with |t| near 3 are kept as findings.

## Ideas
- `032-02.g1.g1_early-decline-near-top-falls` (from F1): Among coins that have fallen over the past 28 days, the nearer the day's close still is to the highest close of the past 56 days, the larger the further fall over the next 5 days.
- `032-02.g1.g2_violent-deep-fall-rebounds` (from F2, F3): Among coins that have fallen over the past 28 days with daily ranges over those 28 days wide compared with the past 90 days, the larger the 28-day fall, the larger the rise over the next 5 days.
- `032-02.g1.g3_near-high-rise-two-days` (from F4): Among coins that have risen over the past 28 days, the closer the day's close is to the highest close of those 28 days, the larger the further rise over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
