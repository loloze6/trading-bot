---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6a908679e54f
---
Fidelity:
- Situation: close above its long moving average, with the close near the top of its recent range and a strong recent rise -> adapted: the above-MA condition is a regime, and range position and rise are graded as one proximity-weighted rise, not as thresholds.
- Comparison: the nearer the high and the stronger the rise, the larger the return -> kept: the position size grows with both.
- Outcome: a larger rise over the following days to two weeks, fading by a month -> adapted: the holding period is dropped, and the return is judged at the two-week horizon.
- Verdict transfer: yes: the forecast grows with exactly the two quantities the idea names, and only inside its condition.
Forecast: The regime is "trending" while the close has been above its 200-bar SMA for at least the current bar. On all other bars the forecast is flat. In the regime, HighProximityMomentumComponent (period 20, return_period 20, convex, power 2) computes the 20-bar percent rise weighted by (1/(1+D))^2, where D is the percent distance below the 20-bar closing high. This is standardised over 60 bars (min 20), then clipped at 0. The forecast is zero when the 20-bar return is not positive. It grows with the size of the rise and shrinks the further the close sits below its recent high. It is never short.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h_config.json
Criterion:
- Horizon: 336 bars
- Main measure: The sample is the non-overlapping 336-bar grid of each window, using bars where the regime is "trending". At each grid bar, take the coin's forward 336-bar return minus that coin's mean 336-bar return over all windows. Regress this excess return on the forecast, pooled over coins. Report the t of the slope, with its count of cases.
- Supporting check: In the book's daily returns, the timing part (the mean gain minus the gain from the market's own rise) is positive.
- Confirm: The confirm rule has two conditions: - the slope's t is 2 or more; - the supporting check is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: These results neither confirm nor reject: - a slope t between -2 and 2; - a slope t of 2 or more with a non-positive timing part; - fewer than 100 grid cases in the regime with a forecast above 0.
