---
idea: 064-01_falling-calm-up-day-fades
brief: 064_falling-calm-scaled-rallies-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: a coin's one-day rise, in units of its own 30-day standard deviation of daily returns, in a falling calm market -> adapted: the rise in 30-day swing units is kept and graded (the larger the rise, the larger the short); the falling calm market is the brief's profile, added by code.
- Comparison: the rise judged against its own 30-day daily swing -> kept
- Outcome: the close falls over the next 3 days, more the larger the rise -> kept
- Verdict transfer: yes: the forecast is short in proportion to the scaled rise, held 3 days, only inside falling calm, so its result is the idea's.
Forecast: One component, `VolatilityScaledReturnComponent` (period 1, vol_period 30): the day's return divided by the standard deviation of the last 30 daily returns. It is standardised over 60 past values (min 20) and clipped at 0, so only up days count. It is then negated. The forecast is 0 on down and flat days. On up days it is negative, and its size grows linearly with the rise in swing units, capped at 20. It is never positive. Code keeps the book flat outside falling calm.
Config: 064-01_falling-calm-up-day-fades_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move of the cases (short bets on the 3-bar grid): the 3-bar return after the signal minus the coin's normal 3-bar drift, in the short direction. Its t is computed with the cases of one day taken together. This is measured before costs, against holding the coin.
- Supporting check: Among the cases, the mean unusual move of the half with the largest |forecast| minus that of the smaller half must be above 0.
- Confirm: Main-measure t ≥ 2 with a positive mean unusual move, and the supporting check above 0.
- Reject: Main-measure t ≤ -2, meaning prices rose after the scaled up days relative to drift.
- Inconclusive: A t between -2 and 2, or t ≥ 2 with the size check not above 0. Fewer than 30 distinct case days in total is also inconclusive.
