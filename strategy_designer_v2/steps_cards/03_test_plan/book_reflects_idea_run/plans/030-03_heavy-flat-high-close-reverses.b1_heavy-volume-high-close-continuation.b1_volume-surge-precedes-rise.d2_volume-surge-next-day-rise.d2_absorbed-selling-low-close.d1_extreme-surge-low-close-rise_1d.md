---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Phase A (runs/BOOK_REFLECTS_IDEA_RUN.md): this plan's config with one rule added: a threshold_filter at 20 after standardise (the situation is present when the score is at least twice its usual size; otherwise no position).
Fidelity:
- Situation: a day's volume heavy relative to its prior 20-day average, with a low close in the day's range -> kept: volume[t] over the mean of the prior 20 days' volume, times (high − close)/(high − low).
- Comparison: the coin's own prior 20-day average volume -> kept: the base excludes bar t (exclude_current 1).
- Outcome: the coin rises over the next day, more for larger surges with lower closes -> kept: a 1-bar long, sized convexly in the surge-times-low-close reading.
- Verdict transfer: yes: the forecast is the idea's own surge × low-close product, sized convexly, so the next-day gain on its positions confirms or rejects the idea directly.
Forecast: The forecast uses VolumeWeightedCloseLocationComponent with volume_period 20, exclude_current 1 and reference "high". It multiplies two things: today's volume divided by the mean of the prior 20 days' volume, and how near the close sits to the day's low (0 at the high, 1 at the low). The forecast is never negative. It is near 0 on ordinary-volume days or on closes near the high, and it grows with both the surge and the low close. The reading is standardised against its own past 60 values, so an average reading is 10. A signed_power step with exponent 2 and pivot 20 then sizes it by the square of the reading (10 becomes 5, 20 stays 20). This is the idea's square sizing with the strongest pivot, so ordinary days sit near flat and the position is concentrated on the largest surges with the lowest closes. A final clip at 0 keeps it long-only. It is ungated and active on every bar.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The cases are bars where the forecast makes a bet (a rise of at least 2 points), pooled over coins and windows. For each case, take the next-day return close[t+1]/close[t] − 1 minus that coin's mean daily return over all its windows. The measure is the mean of this excess return over the cases, with the ordinary t of that mean.
- Supporting check: Among the cases, the mean excess return of the top fifth by forecast must exceed the mean of the other four fifths (Welch t > 0). This shows the gain concentrates on the largest surges with the lowest closes.
- Confirm: The mean excess next-day return is above 0 with t ≥ 2 over at least 100 cases, and the supporting check passes.
- Reject: The mean excess next-day return is below 0 with t ≤ −2 over at least 100 cases.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is a positive main result whose supporting check fails, or fewer than 100 cases.
