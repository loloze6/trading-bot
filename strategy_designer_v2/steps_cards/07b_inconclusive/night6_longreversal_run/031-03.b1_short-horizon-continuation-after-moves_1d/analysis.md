---
line: 7.b inconclusive
backtest: 031-03.b1_short-horizon-continuation-after-moves_1d
idea tested: 031-03.b1_short-horizon-continuation-after-moves
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3057 USD
---
## Findings
- **F1:** The tested effect points the way the idea predicts but is too weak to tell from zero: the slope of the 10-day move beyond drift on the forecast is +0.000362 (t 0.65 clustered by day, 1691 cases on 304 days), and the unusual move per case is +0.49 % (t 0.90), only 0.031 of the coin's usual 14.49 % 10-day move.
- **F2:** Measured on the raw 20-day return instead of the standardised forecast, the effect is about twice as sure but still short of the bar: clustered t 1.24 (1403 cases, 255 days), and t 1.22 on the 20-day return scaled by the coin's recent volatility (1259 cases, 229 days); the forecast and the scaled return correlate at 0.90.
- **F3:** The effect is mixed across periods rather than absent. On the scaled 20-day return, the slope is negative in 2018 (t -1.37), 2022 (t -1.59) and 2023 (t -2.39), and positive in 2019, 2020, 2021, 2024 and 2025 (t +0.34 to +1.20). With unclustered standard errors, 2018 is at t -3.17 and 2023 at t -3.45, against 2020 at t +2.03.
- **F4:** Across coins the slope is positive in 4 of 6 (XRP t 1.55, ETH 1.22, ZEC 0.53, BTC 0.52) and near zero or negative in LTC (t -0.41) and XMR (t 0.30). No single coin carries a clear effect, so six coins over about 210 grid cases each are too few to show a strength near 0.03.
- **F5:** The continuation shows mainly after the largest rises: the top sextile of the scaled 20-day return (mean 20-day return +39.9 %) is followed by +1.70 % beyond drift over 10 days (t 1.30, 210 cases), against -0.21 % after the largest falls (t -0.23). The middle bins are near zero or negative (-1.66 %, t -1.80).
- **F6:** Other horizons do not sharpen the result: the forecast's unclustered slope t is 1.40 at 5 days, 1.07 at 10, 0.05 at 20 and 0.24 at 40. The plan's 10-day horizon is not where a clearer effect hides.

## Ideas
- `031-03.b1.b1_20-day-continuation-all-coins` (from F1, F2, F4): The larger a coin's 20-day return, the more its price moves further in the same direction over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
