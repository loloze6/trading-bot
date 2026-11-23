---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: edf20a924da4
---
Fidelity:
- Situation: a coin's daily high-low range exceeds its norm, by how far -> kept: today's high minus low over its 30-day mean bar range, minus 1.
- Comparison: its average range over the past 30 days -> kept: the mean of high minus low over the last 30 daily bars, today included.
- Outcome: that coin's return over the next 5 days above its usual drift, higher the wider the day -> kept: 5-bar forward return minus the coin's normal 5-bar drift, against the forecast's size.
- Verdict transfer: yes: the forecast is long exactly as far as today's range exceeds its 30-day norm, and flat on narrow days, as the idea states.
Forecast: The forecast starts from RangeCompressionRatioComponent with short_period 1, long_period 30, base "mean_bar_range" and form "compression". Its raw value is 1 minus (today's high-low range / mean daily high-low range over the last 30 bars, today included). That raw value is standardised over its past 60 values (min_periods 20), then negated, which gives a reading proportional to (range ratio − 1). It is then clipped at 0. The forecast is positive and grows linearly with how far today's range exceeds its 30-day norm, capped at +20. It is exactly 0 on days at or below the norm, never negative (long only), and continuous at the norm.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure uses the non-overlapping 5-bar grid of each window (positions 0, 5, 10, ...), cases with forecast > 0 only. Each case's excess return is the coin's 5-bar return minus its normal 5-bar drift, the mean over all its windows. The measure is the OLS slope of that excess return on the forecast, with its t, cases pooled over coins.
- Supporting check: The mean excess 5-bar return of those same cases is above 0. It is measured as the ordinary t of the mean, and must be at least 1.
- Confirm: Slope t >= 2 and the supporting check passes (mean excess return t >= 1), with at least 200 cases.
- Reject: Slope t <= -2 with at least 200 cases.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A slope t >= 2 with the mean excess return t below 1 is inconclusive. Fewer than 200 grid cases with forecast > 0 is inconclusive.
