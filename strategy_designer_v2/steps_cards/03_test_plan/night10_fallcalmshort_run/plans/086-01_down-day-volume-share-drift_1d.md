---
idea: 086-01_down-day-volume-share-drift
brief: 086_calm-downtrend-down-volume-skew-continues
data-instruments: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 9b1f432c9e64
---
Fidelity:
- Situation: a falling, calm market, with recent volume sitting on down days -> kept: the falling calm profile is added by code, and the down-day share of the last 10 days' volume is measured as stated.
- Comparison: a heavier down-day share against a balanced or up-heavy one -> adapted: the share is centred on 0.5 (balanced), and the short grows with the excess above it.
- Outcome: the coin falls further over the next 5 days -> kept: 5 daily bars, short only.
- Verdict transfer: yes: the forecast is the idea's own share, graded against the balanced level, inside the idea's profile, over its 5-day horizon.
Forecast: One component, `DownDayVolumeShareComponent` with `period` 10 and `form` "centred". It gives the share of the last 10 days' volume traded on down closes, minus 0.5. It is standardised over its past 60 values, then negated, then clipped at a maximum of 0. The forecast is negative (short) when down-close volume carries more than half of the 10-day volume, and the short grows with that excess. It is 0 when volume is balanced or up-heavy, so it is never long. The code adds the falling calm profile, so the book is flat outside that profile.
Config: 086-01_down-day-volume-share-drift_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return, minus the coin's mean 5-bar return over all windows, on the raw centred share (`last_history_value`). It is taken on the non-overlapping 5-bar grid of each window, using only cells on in-profile bars. Its t is computed with cells of the same day taken together.
- Supporting check: Over the grid cells with forecast < 0, the mean unusual move in the short direction (the drift removed) is above 0.
- Confirm: The slope is negative with t ≤ -2 (a heavier down share is followed by weaker returns than usual), and the supporting check passes.
- Reject: The slope is positive with t ≥ +2 (heavy down-day volume is followed by stronger returns, so sellers are exhausted).
- Inconclusive: A slope t between -2 and +2, or a confirming slope with a failed check. The test needs at least 30 in-profile grid cells, of which at least 20 have forecast < 0; with fewer it is inconclusive.
