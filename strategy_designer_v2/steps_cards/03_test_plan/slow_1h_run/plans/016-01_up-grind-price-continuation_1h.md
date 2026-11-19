---
idea: 016-01_up-grind-price-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has risen over the past 3 days, and many small hourly gains made a large share of that rise -> kept: the share of the 72-bar net rise not carried by its 3 largest up-hours, 0 when the window did not rise.
- Comparison: many small same-direction hours rather than the few biggest hours -> kept: the residual share is measured against the 3 largest up-hours of the window.
- Outcome: the coin keeps rising over the next 3 days, more so the larger that share -> kept: the forward 72-bar return, judged by how it grows with the share.
- Verdict transfer: yes: the forecast is the idea's own share, it is active only on risen windows, and the outcome is read at the idea's own 3-day horizon.
Forecast: One indicator, `TopGainsShareOfRiseComponent` with period 72 and k 3, form "residual". It is the share of the past 72 hours' net rise that is not carried by its 3 largest hourly gains. It is 0 when the window did not rise, so the forecast is then 0 (flat). It is near 0 when a few hours made the whole rise, and it approaches 1 when the rise is a grind of many small up-hours. It is standardised against its own past 72 values (target 10, cap 20), so the forecast is a long position that grows continuously with the grind share. It is never negative.
Config: 016-01_up-grind-price-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use bars on each window's non-overlapping 72-bar grid where the forecast is above 0, so the coin rose over the past 72 bars. Split them into thirds by forecast, pooled over coins and windows. Take the next-72-bar return of the top third minus that of the bottom third (Welch t), before costs.
- Supporting check: The top third's mean next-72-bar return must exceed the coin's mean 72-bar return over all windows (holding the coin).
- Confirm: The top-minus-bottom difference has a Welch t of 2 or more, and the supporting check passes.
- Reject: The top-minus-bottom difference has a Welch t of -2 or less.
- Inconclusive: The idea is neither confirmed nor rejected in three cases: a t between -2 and 2, a t of 2 or more with a failed supporting check, or fewer than 100 grid cases in either third.
