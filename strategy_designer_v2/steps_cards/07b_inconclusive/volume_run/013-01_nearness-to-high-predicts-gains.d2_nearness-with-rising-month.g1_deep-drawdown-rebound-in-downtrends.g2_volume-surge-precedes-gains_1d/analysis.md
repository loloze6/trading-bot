---
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3055 USD
---
## Findings
- **F1:** The tested slope is on the side the idea predicts but just short of the bar (pooled t = 1.96 over 2443 non-overlapping 7-day cases), and the same positive slope appears at shorter horizons (t = 4.33 at 1 day over 17380 cases, t = 3.19 at 3 days over 5723) while it fades at longer ones (t = 1.32 at 14 days, t = 0.29 at 28 days), so the 7-day test sits where the effect is thinning.
- **F2:** The 7-day effect is weak and uneven across coins and years: per-coin t runs from -0.14 (ETH) and -0.05 (XMR) to 1.61 (XRP) and 1.55 (ZEC), and per-year t runs from -0.79 (2018) to 3.04 (2024), with 2018, 2019 and 2023 negative, so no coin or year shows it clearly on about 300–400 cases each.
- **F3:** The plain effect sits mostly at the extremes of the forecast: the thinnest-volume quintile averages -0.87% excess 7-day return and the heaviest +0.58%, while the middle three quintiles lie between -0.04% and +0.31%.
- **F4:** The effect shows on up days and is mixed on down days: on bars that closed up the slope t is 2.19 (n = 1215), and terciles of relative volume give -0.47%, +0.94% and +1.65% excess 7-day return, while on down days t is 1.36 (n = 1084) and the terciles are non-monotone (-2.01%, +0.22%, -0.92%).
- **F5:** Relative volume signed by the day's direction predicts more clearly than relative volume alone: its 7-day slope t is 2.94 (n = 2299) and its 14-day t is 3.33 (n = 1008), it is positive in all 6 coins at 7 days (t 0.11 to 2.08) and in 7 of 8 years, and its sextiles rise from -0.83% to +1.76% excess 7-day return.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.b1_volume-surge-more-coins` (from F1, F2): The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.b2_heavy-volume-on-up-days` (from F3, F4): The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only on a day the coin closed higher than the day before.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.b3_direction-signed-volume-surge` (from F4, F5): The larger a coin's traded volume over the past day relative to its average over the past 20 days, taken with the sign of that day's return, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
