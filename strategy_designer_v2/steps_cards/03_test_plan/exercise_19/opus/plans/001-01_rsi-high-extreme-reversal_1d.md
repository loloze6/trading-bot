---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme -> adapted: graded short that grows with RSI above 50, sharply damped away from the extreme ("after X" made "while X").
- Comparison: behaviour after extreme versus neutral readings -> adapted: neutral readings give a near-zero position, so extreme bars are judged against the coin's unconditional drift.
- Outcome: price falls back over the following bars -> adapted: the position is held only while RSI stays high; the fixed holding period is dropped.
- Verdict transfer: yes: a short sized by how far RSI sits in its high extreme earns exactly when price retraces after high readings, and loses when it does not.
Forecast: The forecast uses one indicator, the 14-bar Wilder RSI on daily bars, read as 50 minus RSI. It is standardised against its own past 60 values. It is then clipped at 0 from above, so only the high-RSI (short) side remains; it is never positive. Last comes the strongest graded dead zone the guide allows: signed_power with exponent 3 and pivot 20. A standardised reading of -10 becomes -2.5, -15 becomes about -8.4, and -20 stays -20. The forecast is zero when RSI is 50 or below. It is near zero for moderately high RSI and grows smoothly into a large short as RSI reaches its extreme.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward close-to-close return after bars where the forecast is -5 or below. It is taken in excess of that coin's mean 5-bar return over the same window, so the market's own drift is removed. The test is before costs, pooled over coins and windows, on non-overlapping 5-bar blocks so each return counts once.
- Supporting check: The slope of the 5-bar excess return on the forecast, over all bars with a nonzero forecast, using non-overlapping blocks. Reversal means the slope is positive, because a more negative forecast is followed by a lower return.
- Confirm: The mean excess 5-bar return after strong-short bars is negative with t ≤ -2.
- Reject: The mean excess return is positive with t ≥ +2, which means continuation, not reversal. A reject is also recorded if the whole 90% confidence interval of the mean lies inside ±0.5% per 5 bars, meaning no difference from neutral.
- Inconclusive: Any t between -2 and +2 whose 90% interval is not inside ±0.5%. The result is also inconclusive with fewer than 30 non-overlapping strong-short cases in total.
