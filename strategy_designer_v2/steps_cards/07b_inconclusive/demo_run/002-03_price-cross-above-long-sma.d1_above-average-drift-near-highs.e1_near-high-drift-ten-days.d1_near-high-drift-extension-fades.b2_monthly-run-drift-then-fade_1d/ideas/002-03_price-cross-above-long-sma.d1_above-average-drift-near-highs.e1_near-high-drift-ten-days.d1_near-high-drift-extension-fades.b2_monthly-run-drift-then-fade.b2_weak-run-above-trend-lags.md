---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the more its 30-day return has fallen, the larger its fall relative to its usual move over the next 10 days.
Consequence: A trader would cut a long in a coin above its long average when its month-long return turns down, and cut it more the deeper that return goes.
Why:
- F2: The graded rise is carried by the lower and negative runs, not the high ones. The slope of excess 10-day return on s is t=2.38 for s < 8 (n=475) but t=0.10 for s ≥ 8 (n=358). Runs at or below zero above the 200-day average are followed by below-average 10-day returns: −0.024 (t=−2.32, n=142) for s ≤ −4 and −0.042 (t=−2.24, n=49) for s between −2 and 0.
- F1: The fade part of the idea is absent, not reversed: excess 10-day returns stay flat or positive at the largest runs. Tier means are +0.003 for s 8–11, +0.055 for s 11–14, +0.0016 for s 14–17 and +0.021 for s ≥ 17 (n=189). The supporting check is therefore only −0.0095 with t=−0.38 (248 vs 110 cases), while the main slope is positive with t=3.18 on 833 cases.
