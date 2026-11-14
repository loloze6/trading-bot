---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: RSI(14) above 50 becomes a graded long, and `signed_power` makes extremes count most; the hard threshold is dropped.
- Comparison: forward moves after neutral readings -> kept: RSI near 50 gives a forecast near 0, and the criterion contrasts the high-forecast bars with those near-zero bars.
- Outcome: price keeps rising over the following bars -> adapted: "after X" becomes "while X", and the long is held only while RSI stays high.
- Verdict transfer: yes: higher forward returns after the largest RSI-driven longs than after neutral bars confirm the idea, and none or lower rejects it.
Forecast: Take the 14-bar Wilder RSI, read as 50 minus RSI. Standardise it over its past 60 values, then negate it so that RSI above 50 is positive. Clip it at 0, so it is long only, since the idea is only about high extremes. Then apply `signed_power` with exponent 2 and pivot 10. The forecast is 0 when RSI is at or below 50 and small when RSI is just above 50. It grows quadratically as RSI moves further above 50 relative to its usual deviation, reaching 10 at a typical-size deviation and capping at 20 for extremes.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's mean forward 5-bar return after high-extreme bars (forecast ≥ 10), minus its mean forward 5-bar return after neutral bars (forecast < 2.5, RSI near 50). It is pooled over all coins and windows, with overlapping cases thinned to one per 5 bars per coin, before costs.
- Supporting check: The strategy's portfolio return minus holding the coin at the strategy's average exposure, per coin, before costs.
- Confirm: The extreme-minus-neutral difference is at least +1.0% per 5 bars with t ≥ 2 on non-overlapping cases. It must be positive for at least 2 of the 3 coins, and the supporting excess over exposure-matched holding must be positive.
- Reject: The difference is ≤ 0 pooled, or negative for at least 2 of the 3 coins; a significantly negative value (reversal) also rejects this idea.
- Inconclusive: A positive difference below +1.0%, or t < 2, or a coin split that meets neither rule. Fewer than 30 non-overlapping high-extreme cases or 30 neutral cases pooled is also inconclusive.
