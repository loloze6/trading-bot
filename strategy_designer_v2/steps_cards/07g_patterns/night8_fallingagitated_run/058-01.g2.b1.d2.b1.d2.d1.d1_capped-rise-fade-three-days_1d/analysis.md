---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4315 USD
---
## Findings
- **F1:** In the falling agitated profile, the next 3 days' unusual move falls as the day's scaled rise grows. On the grid at offset 0, the slope of strength on the one-day scaled return is -0.27 (t -2.30, 426 cases on 142 days). The slope is negative in each of the four years: 2018 -0.20, 2019 -0.005, 2020 -0.77 (t -4.4), 2021 -0.19.
- **F2:** The fade sits above the tested cap, not inside it. Rises of more than one usual swing are followed by a mean unusual 3-day move of -2.97 % (47 cases). Rises of 0 to 1 swing are followed by -0.04 % (178 cases), a difference with Welch t -1.97. By band, the move is +0.77 % for 0 to 0.5 swings, -1.62 % for 0.5 to 1, -2.71 % for 1 to 2 (t -1.36, 21 days) and -4.76 % above 2 (6 cases). The tested 0-to-1 band's size of +0.35 % (t 0.82) is consistent with this.
- **F3:** The grading in F1 is fragile. It weakens on the other two 3-day grid offsets: slope -0.16 (t -1.55, 139 days) and -0.02 (t -0.19, 141 days). Its strongest year, 2020, holds only 27 case days.
- **F4:** Outside the falling agitated profile the sign is the opposite: 3-day continuation. The slope of strength on the 3-day scaled return is +0.085 (t 1.98, 2260 cases on 397 days), and +0.078 (t 1.88) and +0.051 (t 1.22) on the other offsets. The unusual 3-day move after a 3-day rise above two usual swings is +2.57 % (t 1.48, 50 days). This is not strong enough, across the many angles looked at, to stand as a discovery. The map's 77 long strategies acting in every profile likely already hold it.
- **F5:** The other angles show nothing that stands out once the number of angles is counted:
- **F6:** The book barely trades, so it earns nothing either way. Its mean daily return per window lies between -0.03 % and +0.04 % across w7 to w18. It is in a position on 13 % of the coins' days, with a daily standard deviation of 0.26 %.

## Ideas
- `058-01.g2.b1.d2.b1.d2.d1.d1.g1_large-rise-fade-falling-agitated` (from F1, F2, F3): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its fall over the next three days, with the largest falls after rises of more than one usual swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
