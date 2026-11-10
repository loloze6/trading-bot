---
idea: 002-06_sma-down-regime-negative-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the stretch from a downward 50/200 SMA cross to the next upward cross -> adapted: "after the cross until the next" becomes "while the short SMA is below the long SMA", sized by the size of the gap.
- Comparison: random stretches of the same length -> kept: bar returns inside the stretches are compared with all bars of the same window.
- Outcome: price falls more often and further during the stretch -> kept: forward returns on short-state bars, sign and size.
- Verdict transfer: yes: the short state matches the stretch bar for bar, and the measure reads returns on exactly those bars, whatever the position size.
Forecast: The percent spread between SMA(50) and SMA(200) of the 1h closes (EMASpreadComponent, average "sma"). It is standardised against its own past 200 values, then clipped at a maximum of 0. The forecast is negative (short) only while SMA50 is below SMA200, and it is zero while SMA50 is above. The short grows with how far SMA50 sits under SMA200, up to the cap of -20. It starts near 0 at the cross, so there is no jump.
Config: 002-06_sma-down-regime-negative-drift_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The mean next-bar close-to-close return on bars where the forecast is below 0, minus the mean next-bar return over all bars of the same window. Windows are pooled, and the t-stat uses Newey-West errors with 24 lags so that autocorrelated returns are not counted as separate evidence.
- Supporting check: The share of down bars (negative next-bar return) among short-state bars, minus the share of down bars among all bars.
- Confirm: The pooled return difference is below 0 with a Newey-West t of -2 or lower, and the difference is negative in at least 4 of the 6 windows.
- Reject: The pooled return difference is 0 or higher, or it is positive in at least 4 of the 6 windows. Either result means price does not fall more during the stretches than at random.
- Inconclusive: A negative difference with t between -2 and 0, or a split of 3 windows against 3. A verdict needs at least 10 completed downward-cross stretches and at least 1000 short-state bars across the windows; with fewer, the test is inconclusive.
