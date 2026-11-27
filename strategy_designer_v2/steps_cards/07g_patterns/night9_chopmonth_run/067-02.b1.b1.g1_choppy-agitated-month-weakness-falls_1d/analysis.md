---
line: 7.g patterns
backtest: 067-02.b1.b1.g1_choppy-agitated-month-weakness-falls_1d
idea tested: 067-02.b1.b1.g1_choppy-agitated-month-weakness-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4122 USD
---
## Findings
- **F1:** The tested effect is too small to trade. On the verdict's 457 cases the total move per 7-day case was only +0.03 %, against a trade cost of 0.22 %, because the coins' normal drift ran −0.96 % against the shorts. The unusual move of +0.98 % had t 1.44 over 335 days, and the book earned +0.1 % a year with a Sharpe of 0.05.
- **F2:** In folds B and C, the grid bars in a choppy, agitated market (own 60-day trend, swing above its running median) were followed by below-drift 7-day moves in every 30-day-return tercile. The excess was −9.6 % (t −2.23, 7 days), −5.7 % (t −1.84, 14 days) and −2.6 % (t −0.94, 14 days) from the weakest month to the strongest. This is graded the idea's way, but it rests on only 49 cases, and the full-sample test gave t 0.59 over 133 days.
- **F3:** In a choppy, calm market the same terciles point the other way, toward continuation: −3.1 % (t −1.10, 13 days), +4.0 % (t 1.13, 12 days) and +9.7 % (t 2.19, 6 days). The top tercile stands on 6 independent days, too few to separate from chance.
- **F4:** Across all grid bars, the 30-day return did not order the next 7 days. The quintile excess moves were −0.7 %, −2.5 %, −1.4 %, +2.0 % and +0.9 %, with no |t| above 1.64. In falling and rising markets the terciles were also not monotone, with |t| ≤ 1.69.
- **F5:** Saturday showed the highest mean daily coin return, +0.63 % (t 2.43, 206 days), with Friday at +0.56 % (t 1.81). That is one weekday out of seven, in one of roughly twenty tables examined.
- **F6:** The other bar patterns showed nothing. Next-day excess return after a large one-day move scaled by volatility had all quintiles at |t| ≤ 1.84. Next-day excess by close position in the day's range had |t| ≤ 1.55. Seven-day excess after the past 7 days, by volatility level, by distance from the 30-day high, and by range relative to volatility had at most one bucket with |t| above 2 (t −2.45, a middle quintile, not graded).
- **F7:** The book carried almost nothing. Its mean daily return was near 0 in every window (largest +0.10 % in w16, with a standard deviation of 1.2 %), and it was in a position on 11 % of coin-days.

## Ideas
- No ideas: Across about twenty tables of forecast buckets, profiles, prior moves, volatility, range, weekday and the book, no pattern stood out beyond what that many looks produce by chance. The best candidates (choppy-calm continuation, F3, and the Saturday gain, F5) rest on 6 days or on a single t of 2.4. The tested short already fails on cost, because its total move per case is a tenth of a trade's cost (F1).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
