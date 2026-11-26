---
line: 7.g patterns
backtest: 031-04_fading-volume-after-fall-rebounds_1d
idea tested: 031-04_fading-volume-after-fall-rebounds
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3188 USD
---
## Findings
- **F1:** The book never traded. All 17163 bars of the 6 coins across 141 windows sit in regime "unknown", and 0 of 17163 bars carry a non-zero forecast. Each window is only about 122 bars long (119 to 123), too short for the detector's 365-day volatility to be ready, so the idea was never tested.
- **F2:** Recomputed with each coin's own full-sample volatility, past moves show no lean against or with the following 30 days. The slope of the 30-day excess return on the scaled past return is +0.026 (t 0.72, 388 cases) for a 14-day past, +0.014 (t 0.52, 388) for 30 days, −0.025 (t −1.02, 247) for 60 days, and +0.003 (t 0.09, 106) for 90 days.
- **F3:** Large 90-day falls (scaled return ≤ −1) were followed by +19.7 % excess over 14 days (t 2.98). That rests on only 17 cases, and the same group over 30 days shows −1.4 % (t −0.24, 15 cases), so it does not hold up.
- **F4:** The idea's volume dry-up, as the log of 14-day over 60-day volume, does not predict the next 30 days (slope −0.031, t −0.41, 247 cases). Over 14 days the slope is +0.053 (t 1.13, 423 cases).
- **F5:** A one-day return shows a weak next-day reversal: slope −0.0035 per usual daily move, t −2.20 clustered by day, 8562 cases on 1458 days. It is gone by 3 days (t −1.36). Among about 24 feature-by-horizon slopes tested, this is the only one past |t| 2, which is not enough to stand out from chance.
- **F6:** The Saturday bar shows +0.33 % excess (t 2.95, 1224 cases). That t treats the 6 coins on the same day as separate cases. The coins move largely together, so the same-day cases are far from independent and the evidence is much weaker than t 2.95 suggests. It is also one of 7 weekdays tested.

## Ideas
- No ideas: The book never entered its regime because the 122-bar windows cannot warm up a 365-day volatility (F1). Across the past-move, volume, volatility, range, distance-from-high, one-day-return and weekday angles I looked at, no pattern stood out beyond chance given the number of tests (F2–F6), so no finding supports a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
