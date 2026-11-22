---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 10d8cbead801
---
Fidelity:
- Situation: a flat coin (30-day net move small against its 30-day high-low range), close below that range's middle, with a negative 10-day return -> kept: two regime rules (net move over high-low range at most 0.3; close minus the 30-day high-low midpoint below 0) select the regime, where the size of the 10-day fall sets the short.
- Comparison: the fall is moderate rather than extreme against the coin's own recent 10-day moves -> adapted: the "only while moderate" condition is made graded, as a hump in the fall counted in usual 10-day moves, largest at a usual-size fall and back to 0 at twice that size.
- Outcome: it falls further over the next 5 days -> kept: a short held 5 bars.
- Verdict transfer: yes: the test measures the idea's own conditions and its 5-day outcome, and only the moderate-versus-extreme cut is made graded.
Forecast: The forecast is zero unless the regime is active. The regime is active when the 30-day net move is at most 0.3 of the 30-day high-low range, and the close is below the midpoint of that high-low range (IchimokuCloudPositionComponent with all spans 30 and displacement 0). Inside the regime, x is the 10-day return divided by the mean absolute 10-day return over the last 60 bars, standardised against its own past 70 values. Only falls count: s = max(0, -x), from 0 to 20. The forecast is -(2s - s²/10). It is 0 with no fall. Its size grows as the fall deepens, peaks at a short of 10 at a usual-size fall (s = 10), and shrinks back to 0 at an extreme fall (s = 20, the cap). It is never positive.
Config: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use a non-overlapping 5-bar grid in each window and take the grid bars with forecast below 0. For each case, compute the short-side unusual move: -(close[t+5]/close[t] - 1 - the coin's normal 5-bar drift), divided by the coin's usual 5-bar move. Report the mean over all coins and windows, with its t.
- Supporting check: The same unusual move, weighted by |forecast|, has a mean above 0.
- Confirm: The main measure's mean is above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The main measure's mean is below 0 with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, or a positive t ≥ 2 whose supporting check fails, or fewer than 30 cases.
