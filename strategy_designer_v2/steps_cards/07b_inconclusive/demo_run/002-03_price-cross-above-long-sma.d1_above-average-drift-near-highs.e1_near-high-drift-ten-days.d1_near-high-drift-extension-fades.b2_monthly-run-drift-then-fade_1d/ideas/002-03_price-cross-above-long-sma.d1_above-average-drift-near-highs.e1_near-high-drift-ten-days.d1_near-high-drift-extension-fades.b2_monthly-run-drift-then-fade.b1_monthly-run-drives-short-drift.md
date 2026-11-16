---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 5 days.
Consequence: A trader would size a coin's long by its month-long run while the coin is above its long average, with no trim at extreme runs, and hold it for days rather than weeks.
Why:
- F1: The fade part of the idea is absent, not reversed: excess 10-day returns stay flat or positive at the largest runs. Tier means are +0.003 for s 8–11, +0.055 for s 11–14, +0.0016 for s 14–17 and +0.021 for s ≥ 17 (n=189). The supporting check is therefore only −0.0095 with t=−0.38 (248 vs 110 cases), while the main slope is positive with t=3.18 on 833 cases.
- F3: The effect is strongest at short horizons and fades at longer ones. The slope on s has t=4.01 at 5 days (1674 cases), t=3.00 at 10 days (833), t=0.98 at 20 days (408) and t=1.36 at 30 days (276).
- F4: The effect varies across coins and years. The 10-day slope on s is positive for 5 of 6 coins (ZEC t=2.24, ETH 1.98, BTC 1.69, XRP 0.79, LTC 0.58) and nil for XMR (−0.01). By year, t=2.61 in 2024 and 2.45 in 2025 against −2.10 in 2023, so the market's own moves drown the effect in some periods.
