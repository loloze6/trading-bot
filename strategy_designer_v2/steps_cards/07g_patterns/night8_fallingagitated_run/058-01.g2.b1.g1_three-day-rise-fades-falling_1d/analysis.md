---
line: 7.g patterns
backtest: 058-01.g2.b1.g1_three-day-rise-fades-falling_1d
idea tested: 058-01.g2.b1.g1_three-day-rise-fades-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4340 USD
---
## Findings
- **F1:** Inside the falling agitated profile, the fade belongs to the largest rises only. On the non-overlapping 3-day grid, in-profile rises split into terciles of the scaled 3-day rise give these unusual 3-day moves: small +0.22 % (t 0.15, 38 days), mid +0.16 % (t 0.10, 35 days), large −3.24 % (t −1.88, 29 days). The book's mean forecast was −2.1, −6.4 and −14.9 in the three terciles, so a third of its short exposure sat on rises that gave nothing back.
- **F2:** On in-profile rises, the least-squares slope of the unusual 3-day move on the scaled 3-day rise is −0.0184 (t −2.19, 180 cases on 75 days). The slope is −0.0069 on in-profile falls (t −0.47) and +0.0052 out of the profile (t 2.10, 397 days). The grading of the theme's effect exists, but only on the rise side.
- **F3:** The in-profile slope is at or below zero in all 7 windows with enough cases: w13, w14, w16, w17 and w18 negative, w9 and w15 at +0.0002. The window with the most cases, w18, gives −0.0275 (t −1.43, 22 days).
- **F4:** Across all in-profile grid bars, the 3-day quintiles fall from +3.08 % after the largest falls (t 1.27) to −2.94 % after the largest rises (t −1.83, 29 days). The Spearman correlation of the scaled 3-day rise with the next 3-day move is −0.167 in the profile (p 0.001, n 427) against +0.069 outside it (p 0.001, n 2261). The sign flip between profiles is what the brief claims.
- **F5:** The book earns only when the largest rises fade. On its best 5 % of active coin-days the coin fell 7.6 % on average, and on its worst 5 % it rose 9.8 %. Its mean daily return on days in a position is 0.0048 % against the 0.05 % required, because the many small-rise shorts add cost and nothing else.
- **F6:** The 1-day patterns inside the profile repeat ideas the map already holds, so none is a discovery. The largest 1-day falls are followed by +2.14 % the next day (t 2.89, 116 days), the same as the held "falling agitated daily fall rebound" ideas (047-01, 051-01). The other angles show nothing beyond chance given how many were looked at: weekday (no 1-day weekday |t| above 1.3), own-volatility tercile (|t| ≤ 1.06) and close location (|t| ≤ 1.18).

## Ideas
- `058-01.g2.b1.g1.g1_extreme-rally-fade-falling-agitated` (from F1, F2, F3, F4, F5): In a falling, agitated market, a coin's 3-day rise against the standard deviation of its daily returns over the past 30 days is followed by a fall over the next 3 days that grows faster than the rise itself. The largest rises against usual swing give back several percent, and ordinary rises give back almost nothing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
