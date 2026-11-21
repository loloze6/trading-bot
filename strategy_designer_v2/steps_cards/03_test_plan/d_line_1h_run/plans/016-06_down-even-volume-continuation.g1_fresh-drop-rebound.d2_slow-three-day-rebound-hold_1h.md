---
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin fell over the past 3 days, with some fall over the last 1 day -> adapted: the 3-day fall is a regime on/off condition, and the 1-day fall is graded inside it (72 and 24 bars).
- Comparison: larger 1-day fall against smaller 1-day fall -> kept: the position grows with the size of the 24-bar fall.
- Outcome: the coin rises over the next 3 days, more after larger falls, building across all 3 days -> adapted: the hold-once-for-3-days holding period is dropped, and the rise and its timing are measured over 72 bars.
- Verdict transfer: yes: both the graded rebound and the timing of the rise across the 3 days are measured directly on the recorded closes.
Forecast: A regime rule checks the 72-bar price change. When it is below 0 (the coin fell over 3 days), the bar is in `mean_reversion`; otherwise it is `unknown` and flat. In `mean_reversion`, the 24-bar percent price change is standardised against its past 60 values (about ±10 for a usual move). It is then negated, so a fall reads positive, and clipped at 0. The forecast is long only and grows with the depth of the last day's fall, up to +20. It is 0 when the last day rose, or when the 3-day change is not a fall.
Config: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use non-overlapping 72-bar grid bars in the `mean_reversion` regime, pooled over coins and windows. Regress the excess return close[t+72]/close[t]-1 on the forecast. The excess is over that coin's mean 72-bar grid return across all its windows. The measure is the slope's t.
- Supporting check: Run the same regression with the excess return from close[t+24] to close[t+72] as the target. Its slope must be positive and at least half of the main slope, showing the rise continues after the first day.
- Confirm: Main slope t ≥ 2 and the supporting check passes.
- Reject: Main slope t ≤ -2.
- Inconclusive: Any of these results is inconclusive: - the main t is between -2 and 2; - the main t is ≥ 2 but the supporting check fails; - fewer than 200 grid cases in the regime, or fewer than 100 of them with forecast > 0.
