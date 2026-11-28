---
line: 7.c no effect
backtest: 047-04_falling-agitated-range-scaled-fade_1d
idea tested: 047-04_falling-agitated-range-scaled-fade
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3709 USD
---
## Findings
- **F1:** Across the plan's cases, the market did not fall after up days: the verdict's unusual 3-day move is -0.12 % in the short's direction (t -0.24, 325 case-days, 652 cases). The profile's own drift pushes against the short: in the explore half, profile grid bars rise +1.26 % on average over 3 days (+0.79 % per day), so the total move for a short is -0.31 % per case, against a cost of 0.35 %.
- **F2:** What the market does instead in this profile is rebound after large falls: down days of more than 0.5 of the 30-day mean range are followed by +3.97 % above the profile's 3-day norm (t 2.55, 55 cases over 43 days) and +3.37 % over 1 day (t 2.30, 44 days). This side carries the profile's rank correlation between the scaled move and the next 3 days (rho -0.29, p 0.002, 119 cases), but it is a long move, outside this research's short box.
- **F3:** On the up-day side, which is the tested one, the explore half points the idea's way but weakly and without clean grading. Over 3 days, up days fall 0.65 % (t -0.58), 1.51 % (t -1.12), 1.88 % (t -0.90) and 1.56 % (t -0.91) below the profile norm across the scaled-rise buckets 0–0.25, 0.25–0.5, 0.5–0.75 and above 0.75. Cases where the forecast drops by at least 2 points fall 1.83 % below the norm (t -1.84, 77 days), with no grading across rise size (-2.10 %, -1.17 %, -2.19 %). Since the full-sample verdict is -0.12 %, the check half must lean the other way.
- **F4:** Over 1 day the up-day fade is clearer than over 3. Small up days (0–0.25 range units) fall 2.11 % below the profile's daily norm (t -2.46, 65 days), and the largest (above 0.75) fall 2.64 % below it (t -2.28, 12 days). The middle buckets are -1.02 % (t -1.48) and +0.38 %, so the move is not graded.
- **F5:** Scaling the up day by its 30-day standard deviation of daily returns, the brief's "usual daily swing", grades the 3-day fade monotonically, though no bucket reaches t 1. The unusual moves are -0.95 %, -1.02 %, -1.45 % and -2.42 % for z buckets 0–0.5, 0.5–1, 1–1.5 and above 1.5 (t -0.90, -0.71, -0.72, -0.92; 69, 34, 10 and 11 days).
- **F6:** Where the fade shows, it is uneven. For rises above 0.25 range units, LTC falls -2.20 % over 3 days (t -1.70, 46 days), against XMR -0.88 % (t -0.63) and BCH -1.07 % (t -0.63). By year, 2021 shows -3.15 % (t -2.04, 13 days) while 2018 shows +0.35 % (t 0.15, 22 days). The profile holds only 10–11 % of each coin's bars.

## Ideas
- `047-04.c1_range-scaled-fade-next-day` (from F4, F1, F3): In a falling, agitated market, an up day is followed by a fall over the next day, and the larger the day's rise in units of its 30-day average daily range, the larger that fall.
- `047-04.c2_swing-scaled-rise-fades` (from F5, F3, F6): In a falling, agitated market, an up day is followed by a fall over the next 3 days, and the larger the day's rise in units of the standard deviation of its daily returns over the past 30 days, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
