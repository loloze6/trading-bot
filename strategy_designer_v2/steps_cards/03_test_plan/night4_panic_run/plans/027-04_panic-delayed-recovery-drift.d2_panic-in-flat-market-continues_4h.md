---
idea: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour stretch whose range is several times usual and whose price falls hard -> adapted: the threshold becomes graded, as the 24h fall in usual 24h moves times the 24h range in usual 24h ranges.
- Comparison: the 90-day return before the stretch is close to flat -> kept: a regime rule on the 90-day return ending at the stretch's start, in usual 90-day moves, between -0.5 and +0.5.
- Outcome: lower than usual return from 1 day to 14 days after the stretch ends -> adapted: "after X" becomes "while X", read 1 day after the stretch (lag 6 bars) and held 78 bars short.
- Verdict transfer: yes: the forecast is short in proportion to the panic's extremity exactly 1 day after it ends, only when the prior 90 days were flat, and it is held over the idea's 13-day window.
Forecast: The forecast uses ScaledFallRangeMultipleComponent (period 6, lag 6, window 180). It reads the 24h stretch that ended 24h ago: its fall in usual 24h moves times its range in usual 24h ranges. The value is 0 if that stretch rose. It is standardised over 192 bars, negated (short), and passed through signed_power with exponent 3 and pivot 10. This strongest graded dead zone keeps ordinary down days near 0 and lets extreme panics reach the -20 cap. It is active only in the regime where the 90-day return ending at the stretch's start sits within ±0.5 usual 90-day moves. That return comes from VolatilityScaledReturnComponent (period 540, lag 12, vol_period 20). Elsewhere the forecast is 0. It is never positive. Its size grows with the depth and the range of the panic.
Config: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h_config.json
Criterion:
- Horizon: 78 bars
- Main measure: Cases are the short bets with forecast at or below -10, read once per 78-bar grid cell of each window. For each case, take the coin's 78-bar return from the signal bar minus the coin's normal 78-bar drift over all windows, in the short direction. Report the mean over the cases and its t.
- Supporting check: The mean unusual move of the cases with forecast at or below -15 exceeds that of the cases between -15 and -10 (the more extreme the panic, the weaker the coin).
- Confirm: The mean unusual move in the short direction is above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move in the short direction is below 0 with t ≤ -2 over at least 30 cases, meaning the coin earns more than usual after flat-prior panics.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirming t whose supporting check fails. Fewer than 30 cases over all coins and windows is also inconclusive.
