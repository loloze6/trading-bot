---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only on days the coin closed above its previous day's close.
Consequence: Heavy volume on a rising day would be a reason to hold the coin long for the week, while heavy volume on a falling day would be a reason to stay out despite its one-day bounce.
Why:
- F4: The day's direction splits the volume effect over 7 days. In the top volume-ratio tercile, the excess 7-day return is +1.65% after an up day (t 2.18, 399 cases) and −1.01% after a down day (t −1.35, 319 cases). Thin volume after a down day is also followed by −1.51% (t −2.31, 324 cases).
- F5: High volume on down days gives only a short bounce. Next-day return after a top-quintile-volume down day is +0.92%, yet the excess over the next 7 days is −1.0%. So the large positions the book takes on heavy-volume selling days pay for one day and then give it back, while the book keeps them for the full week.
