---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's one-day fall, relative to its usual daily move over the past 20 days, while its 20-day volatility is high against its own past -> adapted: the high-volatility "when" is a regime (20-day volatility percentile ≥ 0.8 over 100 bars), and the fall is graded by VolatilityScaledReturn(1, 20).
- Comparison: the higher that volatility, the stronger the rebound -> kept: judged in the criterion by comparing the rebound slope across volatility levels inside the regime.
- Outcome: a larger rise over the next day, growing with the fall -> kept: next 1 bar's return, long only after falls.
- Verdict transfer: yes: the forecast buys exactly the vol-scaled one-day falls in high-volatility stretches, sized by the fall, and is judged on the next day's return.
Forecast: A regime turns the idea on only while the 20-day return volatility ranks at or above 0.8 against its last 100 values (VolatilityPercentileRegime, vol_period 20, lookback 100, smooth 5). Otherwise the forecast is 0. Inside the regime, the forecast is the bar's one-day return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturn, period 1, vol_period 20). That value is standardised against its own past 60 values (target 10, cap 20), then negated, then clipped at 0. The forecast is positive and grows with the size of a fall measured in usual moves. It is 0 on up days and outside high volatility. It is never short.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars whose regime is mean_reversion. On those bars, regress the next-bar return minus the coin's mean daily return over all its windows on the bar's forecast. Pool the coins and windows. Report the slope's t.
- Supporting check: Recompute the 20-day volatility percentile from prices. Among bars with forecast > 0, the next-bar return vs forecast slope must be larger where the percentile is ≥ 0.9 than where it is between 0.8 and 0.9 (difference > 0).
- Confirm: The slope's t is ≥ 2 and the supporting check passes.
- Reject: The slope's t is ≤ -2: larger vol-scaled falls are followed by smaller-than-average next-day returns.
- Inconclusive: A t between -2 and 2. A t ≥ 2 with the check failing is also inconclusive. Fewer than 100 bars with forecast > 0 in the regime is inconclusive.
