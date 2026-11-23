---
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours into a 00:00 or 16:00 UTC funding settlement, sized against the coin's usual 2-hour move, after a 7-day run up -> kept: the 2-bar fall in usual 2-bar moves is multiplied by the positive 168-bar return, on the settlement bar only.
- Comparison: the fall against the coin's usual 2-hour move, and growth with the 7-day return before settlement; a flat or falling coin gives no reason -> kept: the product is 0 when the 168-bar return is not positive.
- Outcome: the price rises over the 24 hours after settlement -> kept: the long is held 24 bars from the settlement close.
- Verdict transfer: yes: the forecast is the idea's own sized long, taken at its own clock times, and judged over its own horizon.
Forecast: The forecast is computed only at the close of the bar ending at 00:00 or 16:00 UTC, which is when the coming bar starts at hour 0 or 16. It is flat on every other bar. On those bars it uses MeanAbsScaledFallTimesRiseComponent (fall_period 2, window 720, rise_period 168, rise_lag 0): - the first factor is the 2-hour fall into settlement, counted in the coin's usual 2-hour moves over the last 30 days; - the second factor is the 7-day percent rise, ending at settlement, when that rise is positive. The value is 0 if the coin did not fall over the 2 hours or did not rise over the 7 days. Otherwise it is positive and grows with both the fall and the run up. It is standardised against its own past values (window 500, min_periods 120). It is never negative, so the book is long only. Each bet is held for the 24-hour horizon.
Config: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are bars where the forecast rises by at least 2 points, read once per non-overlapping 24-bar grid cell of each window. For each case, take the coin's 24-bar return from the case's close minus the coin's normal 24-bar drift (all windows together). The measure is the forecast-weighted mean of that excess return over all coins and cases, with its t.
- Supporting check: The Pearson correlation between the case forecast and the case excess 24-bar return is above 0.
- Confirm: The forecast-weighted mean excess return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The forecast-weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with a correlation of 0 or below is also inconclusive. So is any result with fewer than 100 cases in total over all coins and windows.
