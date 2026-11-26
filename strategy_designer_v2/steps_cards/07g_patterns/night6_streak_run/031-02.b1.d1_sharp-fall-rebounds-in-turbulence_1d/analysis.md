---
line: 7.g patterns
backtest: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d
idea tested: 031-02.b1.d1_sharp-fall-rebounds-in-turbulence
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3759 USD
---
## Findings
- **F1:** After a down day, the coin's excess 2-day return rises steadily with its 10-day over 60-day volatility ratio: -0.55 % (t -2.69, 930 cases) at a ratio up to 0.7, +0.08 % (t 0.37, 833) at 0.7–0.9, +0.19 % (t 0.82, 718) at 0.9–1.1, +0.53 % (t 1.88, 708) at 1.1–1.4 and +0.99 % (t 2.08, 347) above 1.4. The tested idea's on/off gate at 1 sits inside a smooth gradient, and down days in the calmest stretches lead to further losses.
- **F2:** After up days the same ratio orders nothing: the excess 2-day return runs -0.08 %, +0.01 %, +0.13 %, -0.21 % and -0.40 % across those five bins, with no |t| above 1 (342 to 988 cases each). The turbulence gradient belongs to falls only.
- **F3:** By length of the current run of same-direction closes, the excess 2-day return after up streaks is -0.32 % after a single up close (t -2.28, 1966 cases), +0.05 % after 2 (t 0.22, 889), +0.04 % after 3 (t 0.15, 418), +0.66 % after 4 (t 1.57, 211) and +0.99 % after 5 or more (t 2.23, 182). Down streaks show no ordering: -2 gives -0.03 %, -3 gives +0.73 % (t 2.34), -4 gives +0.27 %, -5 or more gives -0.32 %. This is the strongest streak pattern but marginal given the many angles examined.
- **F4:** In calm stretches (ratio below 1), moderate days of either sign are followed by underperformance: falls of 0.3–1 usual moves give -0.56 % over 2 days (t -2.67, 934) and rises of 0.3–1 give -0.45 % (t -2.37, 1030). Large calm rises of more than 2 usual moves give +0.97 % (t 2.37, 149).
- **F5:** Next-day excess return by weekday is +0.31 % on Fridays (t 3.76, 2479) and +0.25 % on Thursdays (t 2.63), against -0.30 % on Wednesdays (t -2.70) and -0.24 % on Mondays (t -2.53). The cases are pooled across six coins on the same days, so these t's are overstated.
- **F6:** The book made its money as protection. In the falling years its mean daily return was -3.95 bp in 2018 (holding: -34.70 bp) and -0.56 bp in 2022 (holding: -17.97 bp). It trailed holding on every coin's mean, for example ETH at 2.13 bp against 13.68 bp a day. No 5-day-return or 60-day-volatility-level grouping showed a monotone pattern (largest |t| 2.7, in an isolated bin).

## Ideas
- `031-02.b1.d1.g1_dip-rebound-grows-with-turbulence` (from F1, F2): After a down day, the higher the coin's recent turbulence, measured as the size of its daily moves over the past 10 days against its daily moves over the past 60 days, the more the coin rises over the next 2 days relative to its normal drift.
- `031-02.b1.d1.g2_long-up-runs-keep-rising` (from F3): The longer a coin's current run of consecutive higher daily closes, the more it rises over the next 2 days relative to its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
