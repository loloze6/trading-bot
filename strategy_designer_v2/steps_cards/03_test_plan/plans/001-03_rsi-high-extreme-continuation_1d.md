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
- Situation: RSI at a high extreme -> adapted: graded long position that grows as RSI(14) rises above 50, steepened toward extremes, instead of a fixed threshold.
- Comparison: after high extremes vs after neutral readings -> kept: forward returns after the largest positions compared with returns after bars whose RSI sits near 50.
- Outcome: price keeps rising over the following bars -> adapted: "after the extreme" becomes "while RSI is high", held for as long as the reading lasts.
- Verdict transfer: yes: the forecast is positive only when RSI is high and grows with it, so its forward returns against neutral bars answer the idea directly.
Forecast: The forecast uses RSI(14) on daily closes through RSIPullbackComponent, whose raw value is (50 - RSI) x 0.4. The value is standardised against its own past 60 values, then negated so it is positive when RSI is above 50. It is clipped at 0, so the position is long only while RSI is above 50 and flat otherwise. A signed_power with exponent 2 and pivot 10 then damps mild readings smoothly toward 0 and amplifies extreme ones. The forecast is 0 at or below RSI 50, small near neutral, and grows quadratically as RSI pushes toward its high extremes, capped at 20.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Coin's forward 5-bar return after "extreme" bars minus the forward 5-bar return after "neutral" bars, pooled over the 3 coins and 6 windows, before costs. - Extreme bars: the top 20% of positive forecasts. - Neutral bars: recorded RSI component value within ±4, which means RSI between 40 and 60. - Returns are taken as non-overlapping 5-bar blocks, so overlapping returns count once.
- Supporting check: On bars with a non-zero forecast, the strategy's return minus buy-and-hold's return over the same bars is positive in at least 2 of the 3 coins.
- Confirm: The extreme-minus-neutral difference is positive with t ≥ 2 on non-overlapping returns, and positive in at least 2 of the 3 coins.
- Reject: The difference is negative with t ≤ -2, meaning high RSI is followed by weaker or reversing moves compared with neutral bars.
- Inconclusive: The result is inconclusive in any of these cases: - t lies between -2 and 2; - the result is supported in only one coin; - there are fewer than 30 non-overlapping extreme cases or fewer than 30 neutral cases in the pool.
