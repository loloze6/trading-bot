---
idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: last day's move large relative to its 20-day volatility -> kept: the 1-bar return; dividing it by its own past mean absolute value equals the move over 20-day volatility times the volatility ratio below.
- Comparison: 20-day volatility high against the coin's own history -> kept: the factor σ20 / the 60-bar mean absolute daily move, carried inside that product.
- Outcome: price moves the opposite way over the next 1 day, more so as both grow -> kept: a signed fade sized by the product, held 1 bar.
- Verdict transfer: yes: the forecast is the scaled move times the volatility ratio, faded for exactly one daily bar, as the idea states.
Forecast: Take the coin's 1-day percent return (PriceEvolutionComponent, period 1). Standardise it against the mean absolute daily return of the 60 bars before it (window 60, min_periods 20), then negate it. That value equals the move in units of 20-day volatility times how high the 20-day volatility stands against its 60-bar history. Then apply signed_power with exponent 2 and pivot 10. Small moves, and moves in calm stretches, give a forecast near 0, and the size grows smoothly with both factors. The forecast is negative (short) after an up day and positive (long) after a down day, and 0 on a flat day. It runs on every bar whatever the weekday, with no regime.
Config: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The position's gain on each bar, before costs: postRebalance_current_allocation × (close[t+1]/close[t] − 1 − the coin's mean daily return over all windows). It is pooled over all coins and windows on every bar, and tested with the ordinary t of its mean.
- Supporting check: Split bars by |forecast| into thirds. Compute sign(forecast) × (next-day return − coin mean) in the top third and in the bottom third. The top third minus the bottom third must be greater than 0.
- Confirm: The mean market-adjusted gain has t ≥ 2 and the supporting check's difference is greater than 0.
- Reject: The mean market-adjusted gain has t ≤ −2.
- Inconclusive: Any t between −2 and 2. A t of 2 or more with the check failing is also inconclusive. At least 1000 bars with a non-zero position are required, otherwise the result is inconclusive.
