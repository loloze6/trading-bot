---
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 21:00 UTC close, after a fall over the past 24 hours -> kept: a regime on the coming bar's hour, with the 24-bar return falling below zero.
- Comparison: the fall measured in units of the coin's 7-day hourly volatility, larger fall larger rise -> kept: the 24-bar return over the 168-bar hourly return std times sqrt(24), graded.
- Outcome: the coin rises over the two hours after 21:00, refused when it has not fallen -> adapted: the 2-hour hold is a forecast active on the two decision bars (coming hours 21 and 22) only ("after X" made "while X").
- Verdict transfer: yes: the same time, fall measure, side and two-hour horizon are measured, so a result here is a result for the idea.
Forecast: On bars whose coming hour is 21 or 22 UTC, the forecast is computed from `VolatilityScaledReturnComponent` (period 24, vol_period 168, vol_lookback 1). That value is the 24-hour return over its 7-day hourly volatility scaled to 24 hours. It is standardised against its own past 168 values, negated so that a fall reads positive, and clipped at 0 so the forecast stays long-only. The forecast is 0 when the coin has not fallen over 24 hours. It grows in proportion to the volatility-adjusted fall, up to the cap of 20. On every other hour the regime is null and the forecast is 0 (flat).
Config: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use the decision bars, which are the bars stamped 20:00 UTC and close at 21:00, giving one case per coin-day, pooled over coins and windows. On each, take the 2-bar forward return close[t+2]/close[t]-1 inside its window. Subtract the coin's mean 2-bar return over all its windows, measured on a non-overlapping 2-bar grid. Multiply this excess return by forecast/10. The measure is the ordinary t of the mean of that product.
- Supporting check: On decision bars with forecast > 0, the OLS slope of the excess 2-bar return on the forecast is positive. This tests that a larger fall gives a larger rise.
- Confirm: The idea is confirmed only if both hold: - the main t is 2 or more; - the supporting slope is above 0.
- Reject: The idea is rejected if the main t is -2 or less.
- Inconclusive: Any main t between -2 and 2 is inconclusive. So is a t of 2 or more with a slope of 0 or below. The measure needs at least 200 decision bars with forecast > 0; fewer is inconclusive.
