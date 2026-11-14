---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed above the long SMA -> adapted: "after the cross" becomes "while SMA50 is above SMA200", graded by the size of the spread.
- Comparison: price moves after random points -> kept: forward returns on cross-state bars are compared with the coin's unconditional (buy-and-hold) returns.
- Outcome: price keeps rising, more often and further -> kept: forward close-to-close return of the coin, upward.
- Verdict transfer: yes: a lasting positive spread is the persistent post-cross state, so excess forward gains confirm the idea and their absence or reversal rejects it.
Forecast: The spread (SMA50 − SMA200) / SMA200, using the conventional daily golden-cross pair. It is standardised against its own past 200 values (min_periods 50), then clipped at 0. The forecast is positive while SMA50 is above SMA200 and grows with how far it sits above. It is zero when SMA50 is below SMA200. It never goes short, because the idea is only about the upward cross. It is capped at +20.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Regress the forward 20-bar BTC return on the allocation (forecast / 10), pooled over all 6 windows, before costs. Use a Newey-West t-stat with 19 lags, so overlapping returns count once. A positive slope means returns beyond buy-and-hold that grow with the position.
- Supporting check: Compare the share of positive forward 20-bar returns on bars with allocation > 0 against the share on all bars.
- Confirm: The slope is positive with HAC t ≥ 2, and the supporting hit-rate difference is above 0.
- Reject: The slope has HAC t ≤ −2, meaning reversal after crosses. A second reject is equivalence: the whole 90% confidence interval of the slope lies inside ±2% of 20-bar return per unit of allocation (no difference).
- Inconclusive: Any other result is inconclusive, for example −2 < t < 2 with a confidence interval that crosses outside the ±2% band. The test is also inconclusive if there are fewer than 10 non-overlapping 20-bar blocks with allocation > 0, which is about 200 positive-forecast bars.
