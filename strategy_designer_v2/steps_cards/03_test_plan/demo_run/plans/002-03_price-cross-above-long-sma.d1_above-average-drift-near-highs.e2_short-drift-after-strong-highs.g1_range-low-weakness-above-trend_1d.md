---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day average, close near the low of its 20-day closing range -> adapted: the 200-day condition is a regime, and nearness to the low is the graded position of the close in its 20-bar closing range.
- Comparison: nearer the low versus farther from it, inside the up-trend -> kept: the size of the position grows as the close nears the range low.
- Outcome: a larger fall over the next 5 days -> kept: graded short, judged on 5-bar forward returns against the coin's average.
- Verdict transfer: yes: the test measures this exact condition, range position and 5-day fall, only made graded.
Forecast: The forecast is active only while the close is above its 200-bar SMA (a regime); on other bars it is 0. While active, it reads where the close sits in its 20-bar closing range (Donchian, period 20), from -sf at the low to +sf at the high, standardised over 60 bars (min 20). It is then clipped at a maximum of 0. The forecast is therefore 0 when the close is in the upper half of the range, and an increasingly large short as the close nears the range low. It is never positive.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping grid (positions 0, 5, 10, ... of each window) restricted to bars where regime = trending. On each such bar, multiply (forecast / 10) by the excess 5-bar return, which is close[t+5]/close[t] - 1 minus the coin's mean 5-bar return over all windows. The measure is the mean of these products, tested with the ordinary t of the mean.
- Supporting check: On the same grid, take the active bars with forecast below -10 (close near the range low). Their mean excess 5-bar return minus that of the active bars with forecast 0 must be below 0.
- Confirm: The main-measure t is 2 or more, and the supporting check's difference is below 0.
- Reject: The main-measure t is -2 or less: near the range low in an up-trend, the coin rises more than usual.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with the check failing. At least 100 active grid cases pooled over coins and windows are needed, including at least 30 with forecast below 0; with fewer, the result is inconclusive.
