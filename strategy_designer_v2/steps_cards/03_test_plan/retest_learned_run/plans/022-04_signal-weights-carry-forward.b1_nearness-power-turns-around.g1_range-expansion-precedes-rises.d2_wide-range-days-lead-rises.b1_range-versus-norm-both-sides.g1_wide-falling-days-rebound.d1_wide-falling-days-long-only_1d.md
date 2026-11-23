---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a day the coin closes lower, with its high-low range above its 30-day average range -> adapted: "closes lower" is a regime, and the excess range over that average is a graded size.
- Comparison: the coin's average daily range over the past 30 days -> kept: the 30-day mean bar range, which includes today's bar.
- Outcome: the coin's return over the next 3 days is above its usual drift, long only -> kept: held 3 bars and measured against the coin's drift.
- Verdict transfer: yes: the test measures the same falling-day range excess, the same 3-day long move and the same drift baseline.
Forecast: The regime is active only on bars that close below the prior close; every other bar is flat. On a down day, the component is today's range divided by the mean bar range of the last 30 bars, minus 1 (RangeCompressionRatio, "compression" form, negated). It is standardised against its own past 60 values. It is clipped at 0, so a down day narrower than the norm gives zero and never a short. It is then cubed around pivot 10 (signed_power, exponent 3), so the forecast stays near 0 for ordinary widths and grows fastest on the widest falling days. The forecast is never negative.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move per case: the coin's 3-bar return from the signal bar's close, minus the coin's normal 3-bar drift. Cases are bets (forecast rises of at least 2 points), read on the non-overlapping 3-bar grid of each window, pooled over coins and windows. The measure is the mean of these unusual moves and its t.
- Supporting check: The mean unusual move of cases in the top third of entry forecast exceeds that of the bottom third.
- Confirm: The mean unusual move is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming main measure whose supporting check fails is also inconclusive. Fewer than 30 cases in total is inconclusive.
