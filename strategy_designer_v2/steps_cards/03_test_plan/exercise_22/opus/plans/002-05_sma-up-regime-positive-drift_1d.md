---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch from an upward 50/200 SMA cross to the next downward cross -> adapted: "after the cross until the opposite cross" becomes "while SMA50 is above SMA200", and the position grows with the size of the spread.
- Comparison: random stretches of the same length -> adapted: the return on all bars of the same coin and window, which is what holding the coin earns.
- Outcome: price rises more often and further during the stretch -> kept: the next-bar return of BTC while the forecast is positive.
- Verdict transfer: yes: the forecast is positive exactly on the bars between an up-cross and the next down-cross, so the result applies to those stretches.
Forecast: The (SMA50 − SMA200) / SMA200 spread of daily closes. I use 50/200 because it is the standard golden-cross pair on daily bars and the brief gives no settings. The spread is standardised against its own past 200 values (min_periods 50), then clipped at 0. The forecast is positive only while SMA50 is above SMA200, and it is larger the wider the spread. It is 0 from the down-cross until the next up-cross. It is never negative, because the idea is about up-cross stretches only. It is graded and capped at +20.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The mean next-day log return of BTC on bars where the forecast is above 0, minus the mean next-day log return on all bars (the buy-and-hold baseline). It is pooled over the 6 windows, before costs, with a Newey-West t-statistic (lag 5).
- Supporting check: Within the bars where the forecast is above 0, the slope of the next-day return on the forecast size should be positive. This tests whether a wider spread leads to a larger gain.
- Confirm: The excess mean return on in-stretch bars is positive with t ≥ 2. The supporting check is not required for a confirm.
- Reject: The excess mean return on in-stretch bars is negative with t ≤ −2. That would mean price fades during up-cross stretches.
- Inconclusive: Any result with −2 < t < 2 is inconclusive, including a result near zero. The test also needs enough cases: - at least 100 bars with forecast above 0; - at least 100 bars with forecast at 0; - at least 3 separate up-cross stretches across the windows. If any of these is not met, the test is inconclusive.
