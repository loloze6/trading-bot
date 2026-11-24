---
line: 7.g patterns
backtest: 031-01_near-yearly-low-keeps-falling_1d
idea tested: 031-01_near-yearly-low-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6149 USD
---
## Findings
- **F1:** The day after a daily fall that is large against the coin's own past 30-day swing, the coin tends to rebound, and the rebound grows with the size of the fall: the slope of the next-day excess return on the fall's size is +0.80 % per unit of swing (t 2.22, clustered by day; 3506 down-day cases on 904 days); on rises the slope is flat (+0.11 %, t 0.73, 3612 cases).
- **F2:** Falls of 2 or more past-swing units are followed by a mean next-day excess return of +2.28 % (t 2.35 clustered by day; 194 cases on 77 days), and falls of 3 or more units by +4.66 % (t 1.90; 61 cases on 24 days). That is about 12 times the 0.19 % cost of a trade.
- **F3:** The rebound after falls of 2 or more units appears on every coin (+1.9 % to +3.3 % the next day, 27 to 38 cases each), in 9 of 12 windows and in every year 2018–2021 (+0.8 % to +4.9 %), so no single episode carries it.
- **F4:** The rebound is short-lived: on non-overlapping grids the mean after falls of 2 or more units is +2.2 % over 3 days (t 1.71; 56 cases on 24 days) and −1.4 % over 5 days (t −0.39; 24 cases), and the slope on fall size drops from t 2.22 at 1 day to t 1.13 at 3 days and t 0.08 at 5 days.
- **F5:** The rebound does not come from nearness to the yearly low, which is the brief's situation. After falls of 2 or more units, the next-day excess is +3.8 % in the third farthest from the low and +2.0 % in the nearest third (65 cases each). The 3-day slope on fall size is similar away from and near the low (+0.73 %, t 0.96, against +0.47 %, t 0.67).
- **F6:** The tested idea's own effect is not graded. The top fifth of |forecast| had a 20-day long excess of −5.6 % (t −2.38, 79 cases), but the top fifth of raw proximity to the low had −2.3 % (t −0.88). The middle quintiles were positive (+4.3 %, +4.2 %), so the effect does not rise steadily as the close nears the low. The step-5 size is −1.41 % with t −0.75 on 243 days.
- **F7:** No weekday pattern stands out in next-day excess returns once cases on the same day are taken together (all |t| ≤ 1.11, about 180 days per weekday). The book's 1d returns by weekday are within |t| ≤ 2.0 over 7 weekdays.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `031-01.g2_sharp-fall-next-day-rebound` (from F1, F2, F3, F4, F5): The larger a coin's one-day fall measured against its own typical daily swing over the past 30 days, the more it rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
