---
idea: 026-02_weekend-drop-reverses-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the price falls from Saturday 00:00 to Monday 00:00 UTC -> adapted: the 48-bar loss is read on the bar that closes at Monday 00:00, graded by its size, and zero after a weekend rise.
- Comparison: none -> kept
- Outcome: the price rises over Monday and Tuesday, more after a larger loss -> kept: each bet is held 48 bars from Monday 00:00, with its size set by the loss.
- Verdict transfer: yes: the forecast is exactly the weekend loss, taken only at Monday 00:00 and held for the idea's two days.
Forecast: The forecast uses one component, the 48-bar percent return (`PriceEvolutionComponent`, period 48). On the bar whose close is Monday 00:00 UTC, that return is exactly the change from Saturday 00:00 to Monday 00:00. The value is standardised (window 60, min_periods 20), negated and clipped at 0. It is positive after a weekend fall, larger the deeper the fall (about +10 for a typical 48-bar move), and 0 after a weekend rise. A regime rule makes the forecast live only on that one bar: the coming bar is Monday (weekday 0) and hour 0. Every other bar is flat. The holding period keeps each bet for 48 bars, which covers Monday and Tuesday. The forecast is never short, because the idea only claims rises after falls.
Config: 026-02_weekend-drop-reverses-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is a weekend with forecast > 0 on its Monday 00:00 signal bar. For each case, take the coin's 48-bar return from that bar's close minus the coin's normal 48-bar drift over all windows (the unusual move). Average the cases within each week across coins, then take the t of the mean over weeks.
- Supporting check: Regress the cases' unusual moves on their signal-bar forecast; the slope must be positive.
- Confirm: The mean unusual move is positive with t ≥ 2 and the slope is positive.
- Reject: The mean unusual move is negative with t ≤ -2.
- Inconclusive: The idea is inconclusive when -2 < t < 2, or when t ≥ 2 but the slope is not positive. It is also inconclusive with fewer than 100 weeks that hold a case.
