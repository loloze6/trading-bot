---
idea: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 69355866607f
---
Fidelity:
- Situation: share of the past 30 days the 14-day RSI spent above 50 -> kept
- Comparison: a larger share against a smaller share -> adapted: graded, with the share centred at one half, so a below-half share gives a short position
- Outcome: higher return over the next 14 days -> kept
- Verdict transfer: yes: the forecast is the share itself, so a forward return that rises with it confirms the idea, and one that falls with it rejects it.
Forecast: The forecast is RsiAboveMidlineShareComponent with RSI period 14, a 30-bar window, side "above" and rsi_window 100. Its raw value is the share of the last 30 daily bars with RSI above 50, minus 0.5. It is standardised against its own previous 60 values (min_periods 20), giving a target of 10 and a cap of 20. The forecast is positive (long) when the RSI was above 50 on more than half of the 30 days. It is negative (short) when it was above 50 on fewer than half. It is zero at exactly half. It grows in steps of 1/30 as the share moves towards all or none of the days. It is ungated and applies to every bar.
Config: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: Use non-overlapping bars at positions 0, 14, 28, ... of each window. For each bar, take the coin's 14-bar forward return minus that coin's mean 14-bar return over all windows. Regress this excess return on the bar's forecast, pooling all coins and windows. The measure is the slope's t-statistic.
- Supporting check: none
- Confirm: The slope is positive with t >= 2.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any t between -2 and +2 is inconclusive, including a slope near zero. Fewer than 200 non-overlapping cases with a recorded forecast is also inconclusive.
