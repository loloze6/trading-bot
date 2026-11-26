---
line: 7.b inconclusive
backtest: 060-01.b1.g1_quiet-day-next-fade_1d
idea tested: 060-01.b1.g1_quiet-day-next-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3338 USD
---
## Findings
- **F1:** The tested idea's effect sits inside the falling agitated profile. In the explore half, flat-day cases in a falling agitated market (60-day return below -10 %, 30-day swing above its past-year median) were followed by a next-day drift-adjusted move of -3.67 % (t -2.93, 43 cases on 30 days). Flat-day cases outside that profile moved -0.25 % (t -0.78, 484 cases on 323 days).
- **F2:** With agitation read against a 120-day swing instead, the split is the same. Falling agitated flat days moved -2.93 % (t -3.32, 65 cases, 50 days). Flat days elsewhere moved -0.20 % (t -0.58, 462 cases).
- **F3:** The fade belongs to the flat day, not to the falling agitated market in general. Non-flat days in the same profile were followed by +0.41 % (t 0.55, 167 cases) or +0.62 % (t 0.66, 129 cases).
- **F4:** Outside falling agitated the flat-day effect is weak or reversed. Falling calm moved -0.18 % (t -0.41, 204 cases). Rising calm moved +0.41 % (t 0.47, 92 cases). Choppy moved -0.43 % (t -0.48, 72 cases). This dilution is why the full test's mean of -0.15 % (t -1.26, 3689 cases) stayed short of the bar, and why its size is 0.002 of a usual move.
- **F5:** Inside falling agitated the effect is consistent. It held on the two coins with most cases: BCH -3.08 % (t -2.59, 34 cases) and ZEC -3.19 % (t -3.23, 24 cases). It was negative in every year: 2018 -5.68 % (t -3.43), 2019 -1.86 % (t -2.46), 2020 -1.25 %, 2021 -0.98 %. It also held after up days (-2.85 %, t -2.40) and down days (-3.00 %, t -2.99).
- **F6:** The grading inside the profile is weak, so this evidence is thin. The flatter half of cases moved -3.28 % (t -2.37) against -2.58 % (t -3.02) for the less flat half. The next band of days (|r|/s from 0.25 to 0.5) moved +1.60 % (t 1.89).
- **F7:** In the profile, the move per case is about nine times the 0.32 % cost of a trade. Across the whole test, the unusual move was +0.03 % per case, 0.1 times that cost.

## Ideas
- `060-01.b1.g1.b1_falling-agitated-flat-day-fade` (from F1, F2, F3, F4, F5, F6, F7): In a falling, agitated market, after a day whose close-to-close move is unusually small for the coin, measured as its one-day return against the standard deviation of its daily returns over the past 20 days, the coin falls over the next day; the smaller that move against its recent swing, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
