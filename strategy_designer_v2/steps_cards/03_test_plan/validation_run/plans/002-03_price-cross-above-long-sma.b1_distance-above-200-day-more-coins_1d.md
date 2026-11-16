---
idea: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the close sits above its 200-day SMA, graded by how far above -> kept
- Comparison: the coin's usual 20-day move -> kept
- Outcome: the coin rises more over the next 20 days the further above it sits -> kept
- Verdict transfer: yes: the forecast is the idea's own distance above the 200-day SMA, and it is judged on 20-day returns in excess of the coin's usual 20-day move.
Forecast: The forecast is the percent distance of the close from its 200-day simple moving average, which includes the current close. It is standardised against its own past 200 values (min_periods 50), so a typical distance gives about 10, capped at 20. It is then clipped at 0. The forecast is zero at or below the SMA and positive above it, growing continuously with the distance, so the position grows from zero as the close moves above the average. It is never short.
Config: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Use bars with forecast > 0 on the non-overlapping 20-bar grid of each window. For each, take the coin's 20-bar forward return minus that coin's mean 20-bar return over all windows. Regress this excess return on the forecast and report the slope's t (OLS) and the number of cases.
- Supporting check: Among those positive-forecast grid bars, the mean excess return of the top third by forecast minus that of the bottom third is above 0.
- Confirm: The slope t is at least +2 with at least 100 cases, and the top-minus-bottom-third difference is above 0.
- Reject: The slope t is at most -2 with at least 100 cases.
- Inconclusive: A slope t between -2 and +2 is inconclusive. A t of +2 or more with a top-minus-bottom difference of 0 or less is also inconclusive. Fewer than 100 positive-forecast grid cases is inconclusive whatever the t.
