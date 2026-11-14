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
- Situation: the stretch from the short SMA's up-cross to the next down-cross -> adapted: "after the up-cross" becomes "while SMA50 is above SMA200", graded by the size of the spread.
- Comparison: random stretches of the same length -> adapted: judged against simply holding the coin over the same windows (the unconditional next-bar return).
- Outcome: price rises more often and further during the stretch -> kept: the next-bar return of the coin, upward.
- Verdict transfer: yes: the forecast is long exactly on the bars of the up-cross stretch and flat otherwise, so the gain on those bars against holding is the idea's claim.
Forecast: Uses the spread (SMA50 − SMA200) / SMA200 in percent, on daily closes, at the 50/200 convention. The spread is standardised against its own past 200 values, then clipped at 0. The forecast is positive only while SMA50 is above SMA200, which is the stretch between an up-cross and the next down-cross. Its size grows smoothly from 0 at the cross as the short average pulls further above the long one, capped at 20. It is zero whenever SMA50 is below SMA200, and never negative.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar (next daily close-to-close return; each return is counted once).
- Main measure: The slope of the coin's next-bar return on the bar's allocation, pooled over the 6 windows. The slope is measured against the average return of holding the coin, with a Newey-West t-statistic using 5 lags.
- Supporting check: The mean next-bar return on bars with allocation above 0, minus the mean on bars with allocation equal to 0, with a t-statistic.
- Confirm: A positive slope with t ≥ 2. The supporting difference must also be positive.
- Reject: A slope with t ≤ −2: returns are lower during cross-up stretches, so the cross marks exhaustion.
- Inconclusive: Any t between −2 and 2. The test is also inconclusive with fewer than 300 tested bars, fewer than 100 bars with allocation above 0, or fewer than 3 distinct up-cross stretches across the windows.
