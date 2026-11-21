---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's fall over the 24 hours up to the 20:00 UTC close -> kept: a 24-bar return taken only on the bar whose close is 20:00 UTC (a regime on the hour), long side graded by the fall's depth.
- Comparison: deeper falls against shallower ones ("the more ... the more") -> kept: the position grows with the depth of the fall.
- Outcome: price rises over the next 2 days -> kept: each bet is held 48 bars.
- Verdict transfer: yes: the forecast is the idea's own fall-size relation at the idea's own hour and horizon.
Forecast: On the bar whose close is 20:00 UTC, the coming bar starts at hour 20, and only then is the regime `mean_reversion` active. The forecast is the 24-bar percent price change, standardised over its last 60 hourly values (min 20). It is then negated and clipped at 0. A fall gives a positive forecast that grows with its depth, about +10 for a fall of usual size and capped at +20. A rise gives 0. Every other hour the forecast is 0, and the 48-bar holding period keeps each evening bet open for the 2 days.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the 20:00-close bars with forecast > 0. Taking every other such day per window keeps the 48-bar returns non-overlapping. For each case, take the 48-bar return close[t+48]/close[t]-1 minus the coin's mean 48-bar return over all windows (holding the coin). Regress that excess return on the case's forecast and report the slope's t, pooled over coins.
- Supporting check: The mean excess 48-bar return of the cases in the top third of forecast is above 0.
- Confirm: The slope's t is at least 2 and the top-third mean excess return is positive.
- Reject: The slope's t is -2 or less: deeper falls are followed by weaker 48-bar moves relative to holding the coin.
- Inconclusive: A slope t between -2 and 2, or t ≥ 2 with a top-third mean excess return of 0 or below. A test with fewer than 100 non-overlapping cases is also inconclusive.
