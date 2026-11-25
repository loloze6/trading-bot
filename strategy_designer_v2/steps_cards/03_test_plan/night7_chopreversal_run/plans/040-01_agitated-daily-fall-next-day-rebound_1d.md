---
idea: 040-01_agitated-daily-fall-next-day-rebound
brief: 040_agitated-daily-move-next-day-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's one-day fall, as percent change from the previous close, in an agitated market -> kept: the 1-bar percent change, long only on falls; the agitated profile is added by code.
- Comparison: the larger the fall, the larger the rise -> adapted: graded, so the position grows with the fall's size against its usual daily move.
- Outcome: the price rises over the next day -> kept: 1-bar horizon on daily bars.
- Verdict transfer: yes: the forecast is the fall's size in agitated bars, so a next-day rise that grows with it confirms the idea, and a next-day fall that grows with it rejects it.
Forecast: The forecast uses one indicator, the 1-bar percent change of the close (PriceEvolutionComponent, period 1). It is standardised against the mean absolute size of its last 60 daily changes (min_periods 20), then negated, then clipped at 0. The forecast is positive only on down days and grows linearly with the size of the fall: an average-sized fall gives about +10, and the forecast is capped at +20. It is 0 on up days and flat days. Outside the agitated profile the book is flat (code adds this).
Config: 040-01_agitated-daily-fall-next-day-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the slope of a regression of the next-day return minus the coin's mean daily return (over all windows) on the forecast. Its t has cases grouped by day.
- Supporting check: On bars with forecast > 0, the mean next-day return minus the coin's mean daily return is above 0.
- Confirm: The slope's t is 2 or more and the supporting mean is above 0.
- Reject: The slope's t is -2 or less: larger falls are followed by smaller or more negative next-day moves than the coin's drift.
- Inconclusive: Any slope t between -2 and 2, or a t of 2 or more with a supporting mean at or below 0. A verdict needs at least 100 bars with forecast > 0 across all coins and windows.
