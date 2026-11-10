---
idea: 002-02_sma-downcross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: The percent spread between the 50-bar and 200-bar simple moving averages of the close on 1h bars, (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own past 200 values: the latest spread is divided by the mean absolute spread of the 200 bars before it, times 10, and capped at ±20. Only the negative side is kept. The forecast is negative (short) while SMA50 is below SMA200, and the short grows the further the short average sits below the long one. It is zero while SMA50 is at or above SMA200. It never goes positive.
Config: 002-02_sma-downcross-downward-drift_1h_config.json
Confirm: Use the 24-bar forward log return of BTC. On bars where the forecast is below 0, its mean minus the window's unconditional mean 24-bar return is the excess, before costs. Sample every 24th bar so overlapping returns count once, and pool the 6 windows. The idea is confirmed if this excess is negative with t ≤ −2 and negative in at least 4 of the 6 windows. Supporting check: on those same sampled bars, the share of negative 24-bar returns exceeds the unconditional share.
Reject: The idea is rejected if the pooled excess 24-bar return on short-forecast bars is zero or positive. A positive excess means price tends to reverse up after the downward cross, which marks exhaustion rather than the start of a trend.
Inconclusive: The excess is negative but with t between −2 and 0, or it is negative pooled but in fewer than 4 of the 6 windows.
Deviation: "After the short average crosses below the long one" becomes "while SMA50 is below SMA200". The short is sized by how far the short average sits below the long one, not by how recent the cross is. Bars long after a cross count as much as bars just after it. The 50/200 settings are convention, since the brief gives none.
