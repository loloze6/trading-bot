---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-05_sma-up-regime-positive-drift_config.json
Confirm: Over a 20-bar horizon, forecast-weighted returns (forecast at bar t times the BTC return from t to t+20) are positive, and the portfolio's gain exceeds buy-and-hold of BTC (before costs). Gains should also grow with the size of the position: the bars in the top tercile of positive forecast should be followed by higher mean 20-bar returns than the lower tercile, and the bars with the most negative forecasts by lower returns than the bars with small forecasts.
Reject: Over the 20-bar horizon, forecast-weighted returns are zero or negative, or the portfolio does not beat buy-and-hold BTC (before costs). Rejection is also supported if returns after large positive forecasts are lower than after small ones (reversal after crosses).
Inconclusive: The portfolio beats buy-and-hold but forecast-weighted 20-bar returns do not grow with position size, or the gain comes from a few large episodes; or the portfolio's return is positive but within buy-and-hold's error range (the long-only market drift explains it).
Deviation: The idea is an event-based stretch (from an upward cross to the next downward cross, long only). The config instead holds a graded position proportional to the standardised SMA50-SMA200 spread on every bar. It is signed (short when the short average is below the long), and its size varies with the spread, not a fixed level across the stretch. It tests "the sign and size of the spread predict the following 20-bar return", not returns measured from each cross to the next.
