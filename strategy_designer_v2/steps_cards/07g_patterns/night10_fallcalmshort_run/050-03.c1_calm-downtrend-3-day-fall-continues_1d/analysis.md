---
line: 7.g patterns
backtest: 050-03.c1_calm-downtrend-3-day-fall-continues_1d
idea tested: 050-03.c1_calm-downtrend-3-day-fall-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3921 USD
---
## Findings
- **F1:** Within the falling calm profile, 3-day falls (79 non-overlapping 3-bar cases on 58 days, BTC, XMR and XRP) were followed by a 3-day unusual move of +1.28 % in the short direction, but the day-clustered t is only 1.61; at 5 days it was +2.45 % with t 1.73 (40 cases, 28 days). The carry-on has the brief's sign but cannot be told from chance.
- **F2:** The carry-on after 3-day falls does not grow with the fall's size. The Spearman correlation between the scaled fall and the short-direction move is -0.002 (p 0.99) at 3 days and 0.12 (p 0.46) at 5 days. The larger-fall half earned +1.31 % against +1.25 % for the smaller half at 3 days. This matches the verdict's supporting check of -0.11 %, so the graded part of the theory is absent.
- **F3:** Across all in-profile grid points, the 3-day scaled return ranks with the next 3-day unusual move at Spearman 0.20 (p 0.018, 139 cases). Much of that comes from rises, not falls: after 3-day rises the coin went on up by +1.48 % (t 1.73, 60 cases) at 3 days and +2.41 % (t 2.03, 39 cases) at 5 days. A rise cannot be taken short, so this is outside the run's short-only box.
- **F4:** In round 1's quintiles of the scaled 3-day return, the mean unusual move rises from -1.60 % (t -1.35) in the deepest-fall fifth to +2.10 % (t 1.79) in the largest-rise fifth. The slope is two-sided, but no single quintile reaches |t| 2.1.
- **F5:** Several other angles showed nothing that stood out against the number of cuts made (35 bins on 7 measures in round 1, plus weekday cuts and terciles). These were the 1-day scaled return, the close location, the scaled range, the volume ratio, the depth below the 20-day high, the weekday and the 60-day trend depth. The largest |t| were 2.6 (volume-ratio middle fifth, 20-day drawdown middle fifth) and 2.2 (Monday 1-day move -1.0 %), each in a non-monotone pattern. The 60-day trend terciles after falls ran deep +2.42 % (t 2.24), mid -0.81 %, shallow +2.94 %, which is not graded.
- **F6:** The book's trades lost on every coin. Mean net trade returns were -1.37 % on BTC (112 trades), -1.86 % on XMR (88) and -0.55 % on XRP (89), with medians -1.20 %, -2.78 % and -1.06 %. The coins spent only 10 %, 18 % and 21 % of their bars in the falling calm profile. The idea's measured unusual move per case (+0.19 %) is 0.7 times the 0.29 % cost of a trade.

## Ideas
- No ideas: Inside the falling calm profile on the short side, the only consistent pattern is that 3-day falls are followed by further weakness (+1.3 % to +2.5 %, t 1.6 to 1.7), and it neither grows with the fall's size nor clears chance across the many angles examined (F1, F2, F5). Its clearer two-sided form rests partly on rises, which fall outside the short-only box (F3, F4).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
