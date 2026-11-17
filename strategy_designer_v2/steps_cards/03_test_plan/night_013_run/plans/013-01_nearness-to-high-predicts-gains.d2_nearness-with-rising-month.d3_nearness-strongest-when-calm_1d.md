---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d3_nearness-strongest-when-calm
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close near its 52-week high, only while the 30-day return is positive -> kept: DistanceFromHighComponent(365) for nearness, with a regime rule on PriceEvolutionComponent(30) above 0.
- Comparison: the link is stronger the calmer the last 20 days' daily moves are against the past year -> replaced: only a regime cut or an added term is possible, not a graded interaction.
- Outcome: higher return over the next 7 days, rising with nearness and the 30-day return -> kept: 7 bars.
- Verdict transfer: no: without the graded calm-times-nearness interaction, the test cannot confirm or reject the idea's claim that calm strengthens the link.
Reason: The forecast is a weighted sum of components, so it cannot multiply nearness to the high by a calmness measure. A regime cut on VolatilityPercentileRegimeComponent would turn a graded interaction into on/off, and vol_normalize uses the 24-bar price stddev times the close, a different quantity. All the inputs are in the coin's own closes, so one component could compute this.
