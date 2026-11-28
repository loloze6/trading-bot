---
line: 7.b inconclusive
backtest: 047-03.c1_rally-near-30-day-high-fades_1d
idea tested: 047-03.c1_rally-near-30-day-high-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2221 USD
---
## Findings
- **F1:** The test's main slope is on the idea's side but short of the bar (t -1.18, 562 cases on 288 days, mean unusual move +0.03 % with t 0.05). In the explore half only three coins ever reached the falling-agitated profile: 330 profile days (LTC 169, XMR 94, BCH 67). That leaves 57 non-overlapping 3-day up-day cases there. Five of the eight coins tested (AVAX, INJ, GRT, DOGE, FIL) contributed nothing in these windows, and BCH, GRT and FIL are not among the 19 coins the data offers.
- **F2:** The proximity grading is not monotonic over 3 days. By quartile of distance below the 30-day closing high, the shorted 3-day unusual move is +3.9 % near the high (t 2.16, n 14), +1.5 % in q2 (t 1.26), −3.7 % in q3 (t −2.40) and +1.8 % deepest (t 0.65). The pooled slope on proximity is only t −0.50 over 57 cases, so the effect is mixed rather than absent.
- **F3:** The next day carries more of the proximity effect than three days do. Up days in the nearest two quartiles fall the next day by 1.8 % (t 3.33, n 42) and 2.2 % (t 2.65, n 41), against −0.4 % and +0.7 % in the farther two. The pooled 1-day slope on proximity is t −1.24 (165 cases).
- **F4:** The size of the up day's rise grades the 3-day fall much better than proximity does. The slope of the drift-adjusted 3-day return on the day's return is t −3.07 (57 cases), against t −0.50 for proximity. The largest-rise quartile falls 5.5 % in excess over 3 days (t 3.57, n 11), the smallest rises 2.4 % (t −0.98).
- **F5:** The brief's own two-way next-day fade is strong in this profile. Over all 330 profile days, the next-day drift-adjusted return on the day's return has a slope of −0.26 (t −6.07). The market itself drifts up (mean 3-day return +0.7 % to +0.9 % per coin), which works against every short case.
- **F6:** Per case the total move is −0.15 % against a trade cost of 0.35 %. Even confirmed on more data, the proximity idea as tested would need a much larger move per case to pay, which the large-rise cases of F4 come closer to.

## Ideas
- `047-03.c1.b1_rally-near-high-fade-more-coins` (from F1, F2, F3): In a falling, agitated market, the closer a coin's close on an up day is to its highest close of the past 30 days, the larger its fall over the next three days.
- `047-03.c1.b2_large-rise-fades-three-days` (from F4, F5, F6): In a falling, agitated market, the larger a coin's one-day rise, the larger its fall over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
