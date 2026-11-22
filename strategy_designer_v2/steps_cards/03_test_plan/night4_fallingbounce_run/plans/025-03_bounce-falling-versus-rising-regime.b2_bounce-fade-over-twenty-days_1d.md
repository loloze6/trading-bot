---
idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a one-day rise of several usual daily moves (the day's return over the std of the last 20 daily returns) -> adapted: the threshold "several" is made graded, as the volatility-scaled 1-day return kept on its rise side only, with a cubic dead zone.
- Comparison: 90-day return negative against positive -> kept: a regime rule on the 90-day return's sign.
- Outcome: the 20-day return is lower after bounces in 90-day fallers than in 90-day risers, and the gap widens with the rise -> kept: each bounce is held 20 bars, long in risers and short in fallers, sized by the rise.
- Verdict transfer: yes: the test compares the 20-day returns after the same graded bounces split by the 90-day sign, and it checks that the gap grows with bounce size.
Forecast: The 90-day percent return (PriceEvolution, period 90) picks the regime. Below 0 it is `mean_reversion`; at or above 0 it is `unknown`; nothing else is selected. In both regimes the component is the same one-day volatility-scaled return (VolatilityScaledReturn, period 1, vol_period 20). It is standardised over 60 bars (min 20) and clipped at 0, so it is zero on down days. A cubic dead zone (signed_power, exponent 3, pivot 20) then makes small rises nearly zero and lets the forecast grow steeply with larger ones. The forecast is positive (long) in a 90-day riser and negated (short) in a 90-day faller. Its size grows with the bounce. It is zero on any day that did not rise. Each bounce is held for 20 bars.
Config: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Cases are the bets (forecast rises of at least 2 points), read once per 20-bar grid cell. For each case, take the coin's 20-day return minus its normal 20-day drift. Compare long-regime cases (90-day up) against short-regime cases (90-day down), as up minus down, with Welch's t.
- Supporting check: Within each group, split the cases at the median of |forecast|. The up-minus-down gap among the larger bounces must exceed the gap among the smaller ones.
- Confirm: The up-minus-down difference has Welch t >= 2 and the supporting check passes (larger-bounce gap > smaller-bounce gap).
- Reject: The up-minus-down difference has Welch t <= -2, meaning returns after bounces in fallers are reliably higher than in risers.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the gap not widening for larger bounces. A result is also inconclusive with fewer than 30 cases in either group.
