---
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
idea tested: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4182 USD
---
## Findings
- **F1:** Each coin's mean next-hour return is far above its other hours in the bars starting 20:00 and 21:00 UTC (+0.000545, t 6.75, and +0.000436, t 5.66, about 17,400 bars each), while the 02:00 and 13:00 UTC bars are negative (−0.000277, t −3.80, and −0.000356, t −3.80); pooled coins move together, so these t-values are inflated, but 20:00 still stands well above the many angles looked at.
- **F2:** Rises built as a grind continue: among 3-day rises, the tercile with the highest path efficiency (|72-bar net log move| over the sum of |hourly log moves|) is followed by +0.0084 excess 72-bar return (t 2.85, 955 non-overlapping cases), against −0.0039 (t −1.42) for the least efficient, most jumpy rises.
- **F3:** Falls built from choppy, back-and-forth hours keep falling rather than reversing: among 3-day falls, the lowest-efficiency tercile is followed by −0.0091 excess 72-bar return (t −3.38, 890 cases), while the middle and grind terciles are flat (+0.0010 and +0.0001).
- **F4:** The tested rebound lives only in the top fifth of the forecast: active cases in the top forecast quintile earn +0.0112 excess 72-bar return (t 3.30, 553 cases), while the 2nd and 3rd quintiles lose −0.0065 (t −1.79) and −0.0082 (t −2.14), and active cases overall return −0.0015 against +0.0014 for inactive ones.
- **F5:** Across all grid cases, the past 72-bar return gives a U-shape: the middle quintile is followed by −0.0071 excess (t −3.20, 1107 cases), the top quintile by +0.0055 (t 1.85) and the bottom by +0.0016.
- **F6:** The book still loses: mean daily return is −0.000787 against +0.001179 for holding (Sharpe −1.04, 2,898 book-days, correlation with holding 0.67), on 61,365 trades with a median length of 8 hours and a mean of −0.47% before fees and −0.57% after; per bar the position's gain is 0.000005 against a market part of 0.000013, so its timing is negative.
- **F7:** The active cases are dominated by one year: in 2018 they return −0.0217 excess (t −4.58, 417 cases), while every later year lies between −0.0067 and +0.0105 with no year beyond |t| 1.7.

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g1_grind-up-rise-continues` (from F2): When a coin has risen over the past 3 days, the more evenly that rise was spread across its hourly steps (net 3-day move large relative to the sum of its absolute hourly moves), the more the coin keeps rising over the next 3 days.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g2_choppy-fall-keeps-falling` (from F3, F4): When a coin has fallen over the past 3 days, the more that fall was made of back-and-forth hourly swings (net 3-day move small relative to the sum of its absolute hourly moves), the more the coin keeps falling over the next 3 days.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g3_only-extreme-falls-rebound` (from F4, F5, F6): When a coin has fallen over the past 3 days, its rebound over the next 3 days grows with how extreme the combined depth of its 3-day fall and its fresh 1-day drop is relative to its recent swings, and the coin keeps falling after mid-sized combined falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
