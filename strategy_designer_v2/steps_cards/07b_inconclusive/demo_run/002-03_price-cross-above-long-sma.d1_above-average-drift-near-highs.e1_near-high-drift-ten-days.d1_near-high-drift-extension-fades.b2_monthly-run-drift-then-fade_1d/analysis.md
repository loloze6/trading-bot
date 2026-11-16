---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2072 USD
---
## Findings
- **F1:** The fade part of the idea is absent, not reversed: excess 10-day returns stay flat or positive at the largest runs. Tier means are +0.003 for s 8–11, +0.055 for s 11–14, +0.0016 for s 14–17 and +0.021 for s ≥ 17 (n=189). The supporting check is therefore only −0.0095 with t=−0.38 (248 vs 110 cases), while the main slope is positive with t=3.18 on 833 cases.
- **F2:** The graded rise is carried by the lower and negative runs, not the high ones. The slope of excess 10-day return on s is t=2.38 for s < 8 (n=475) but t=0.10 for s ≥ 8 (n=358). Runs at or below zero above the 200-day average are followed by below-average 10-day returns: −0.024 (t=−2.32, n=142) for s ≤ −4 and −0.042 (t=−2.24, n=49) for s between −2 and 0.
- **F3:** The effect is strongest at short horizons and fades at longer ones. The slope on s has t=4.01 at 5 days (1674 cases), t=3.00 at 10 days (833), t=0.98 at 20 days (408) and t=1.36 at 30 days (276).
- **F4:** The effect varies across coins and years. The 10-day slope on s is positive for 5 of 6 coins (ZEC t=2.24, ETH 1.98, BTC 1.69, XRP 0.79, LTC 0.58) and nil for XMR (−0.01). By year, t=2.61 in 2024 and 2.45 in 2025 against −2.10 in 2023, so the market's own moves drown the effect in some periods.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.b1_monthly-run-drives-short-drift` (from F1, F3, F4): While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 5 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade.b2_weak-run-above-trend-lags` (from F2, F1): While a coin's close is above its 200-day average, the more its 30-day return has fallen, the larger its fall relative to its usual move over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
