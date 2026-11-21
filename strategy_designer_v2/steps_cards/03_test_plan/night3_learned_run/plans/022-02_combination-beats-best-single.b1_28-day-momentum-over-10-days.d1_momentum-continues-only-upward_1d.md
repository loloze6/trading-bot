---
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day return is a rise, larger rise stronger -> adapted: the on/off "only while a rise" becomes graded, with the long size growing from 0 as the rise grows.
- Comparison: none -> kept
- Outcome: a 10-day gain that grows with the size of the rise -> kept
- Verdict transfer: yes: the forecast is the 28-day rise itself, zero after a fall and held for 10 days, so its 10-day results judge the idea directly.
Forecast: One indicator, the 28-bar percent return of the close (`PriceEvolutionComponent`, period 28), on every bar with no regime. It is standardised against its own last 60 values, so a usual-sized 28-day move reads about 10, and it is capped at 20. It is then clipped at 0, so a 28-day fall gives exactly 0 (flat, never short). The forecast is positive and grows in proportion to the size of the 28-day rise, and is zero whenever the coin fell over 28 days.
Config: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On each window's non-overlapping 10-bar grid, the coin's 10-day return minus its normal drift (its mean 10-day return over all windows) is regressed on the forecast. The measure is the OLS slope's t across all coins' grid cases, before costs.
- Supporting check: Among grid cases with forecast > 0 only, the mean of the 10-day return minus normal drift is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2 is inconclusive. A t of 2 or more with the check failing is also inconclusive. Fewer than 100 grid cases with forecast > 0 is inconclusive whatever the t.
