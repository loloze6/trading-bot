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
- Situation: RSI at a high extreme -> adapted: graded with signed_power, so the position grows with RSI above 50 and is near zero close to 50.
- Comparison: rise after extremes vs after neutral readings -> kept: judged in the criterion against bars with RSI 40 to 60.
- Outcome: price keeps rising over the following bars -> adapted: "after the extreme" becomes "while RSI is high"; the rise is measured over a fixed 5-bar horizon.
- Verdict transfer: yes: a confirm or reject on the high-RSI long position compared with neutral bars answers the idea as stated.
Forecast: Use the 14-bar Wilder RSI on daily bars (RSIPullbackComponent, signed (50 - RSI) x 0.4), standardised over its past 60 values (min 20). It is negated so high RSI reads positive, squared with signed_power (exponent 2, pivot 10) so moderate readings shrink towards zero and extremes are amplified, then clipped at 0, so the strategy is long only. The forecast is 0 when RSI is at or below 50. Above 50 it grows smoothly, and its largest values come at the highest RSI readings.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: For each coin, the forward 5-bar close-to-close return after "extreme" bars minus the same return after "neutral" bars, pooled over the three coins. Extreme bars are those in the top 20% of positive forecasts. Neutral bars are those where the recorded RSI component value is within ±4, which is RSI 40 to 60. Overlapping 5-bar returns are counted once, by thinning to one case per 5-bar span (or using Newey-West with lag 4). Measured before costs.
- Supporting check: The strategy's per-bar return minus forecast/10 times the coin's average per-bar return over the same window. This is the timing gain over holding the coin at the same average exposure, and it should have the same sign as the main measure.
- Confirm: The extreme-minus-neutral difference is positive with t ≥ 2. It must be positive on at least 2 of the 3 coins, and the supporting timing gain must be above 0.
- Reject: The difference is negative with t ≤ -2, meaning lower returns after high extremes than after neutral bars (no continuation or a reversal), with the timing gain at or below 0.
- Inconclusive: A t between -2 and 2, or a confirm or reject sign that the supporting check contradicts. The test also needs at least 30 non-overlapping extreme cases and 30 non-overlapping neutral cases pooled over the three coins; with fewer, it is inconclusive.
