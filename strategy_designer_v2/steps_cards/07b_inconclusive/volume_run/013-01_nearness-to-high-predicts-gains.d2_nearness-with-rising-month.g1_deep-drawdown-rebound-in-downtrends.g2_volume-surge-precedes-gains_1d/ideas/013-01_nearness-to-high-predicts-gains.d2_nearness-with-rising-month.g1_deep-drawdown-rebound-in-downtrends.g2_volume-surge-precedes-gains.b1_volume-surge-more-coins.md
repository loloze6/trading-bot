---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days.
Consequence: A rise in volume would favour holding a coin long over the next week, and unusually thin volume would be a reason to stay out.
Why:
- F1: The tested slope is on the side the idea predicts but just short of the bar (pooled t = 1.96 over 2443 non-overlapping 7-day cases), and the same positive slope appears at shorter horizons (t = 4.33 at 1 day over 17380 cases, t = 3.19 at 3 days over 5723) while it fades at longer ones (t = 1.32 at 14 days, t = 0.29 at 28 days), so the 7-day test sits where the effect is thinning.
- F2: The 7-day effect is weak and uneven across coins and years: per-coin t runs from -0.14 (ETH) and -0.05 (XMR) to 1.61 (XRP) and 1.55 (ZEC), and per-year t runs from -0.79 (2018) to 3.04 (2024), with 2018, 2019 and 2023 negative, so no coin or year shows it clearly on about 300–400 cases each.
