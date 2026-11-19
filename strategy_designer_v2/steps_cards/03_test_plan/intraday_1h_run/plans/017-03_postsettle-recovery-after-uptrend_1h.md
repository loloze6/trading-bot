---
idea: 017-03_postsettle-recovery-after-uptrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin with a strong 3-day run up, at each funding settlement time (00:00, 08:00, 16:00 UTC) -> adapted: "strong" made graded by the size of the 72-bar rise (long only), with a clock regime holding only the 2 bars after each settlement.
- Comparison: the stronger the 3-day rise, the larger the recovery -> kept: the position grows with the 72-bar rise.
- Outcome: the return over the 2 hours after settlement is positive -> kept: a 2-bar forward return from the settlement close, against holding the coin.
- Verdict transfer: yes: the test measures this exact 2-bar post-settlement return, graded by the same 3-day rise.
Forecast: The detector reads HoursToSettlementComponent. It selects `trending` while the coming bar starts at a settlement hour or one hour after it (value 7 or 8). That covers the bars stamped 23:00, 07:00 and 15:00, and the bars stamped 00:00, 08:00 and 16:00. On every other bar the regime is flat. In `trending`, the forecast is the 72-bar (3-day) percent rise from PriceEvolutionComponent(72). It is standardised over its own past 72 values and clipped at 0, so it is long only. It is zero when the coin did not rise over 3 days, and it grows with the size of the rise, up to the cap of 20.
Config: 017-03_postsettle-recovery-after-uptrend_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the settlement entry bars: hours 23:00, 07:00 and 15:00 with regime `trending` and forecast > 0. For each case, take the excess return close[t+2]/close[t]-1 inside the window, minus the coin's mean 2-bar return over all windows. Regress that excess return on the recorded forecast and report the slope's t-statistic. Cases are 8 hours apart, so they do not overlap.
- Supporting check: The forecast-weighted mean excess 2-bar return over the same cases is above 0.
- Confirm: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2, or a slope t of 2 or more with a forecast-weighted mean excess return of 0 or below. The test needs at least 300 cases pooled across coins and windows.
