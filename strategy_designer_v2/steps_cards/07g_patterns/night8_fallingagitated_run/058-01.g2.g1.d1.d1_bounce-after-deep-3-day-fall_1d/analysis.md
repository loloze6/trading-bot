---
line: 7.g patterns
backtest: 058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d
idea tested: 058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3988 USD
---
## Findings
- **F1:** In the falling agitated profile, a coin's next-day return runs against its day's return scaled by its 30-day swing (Spearman rho -0.216, p < 0.001, 1,102 bars), and this is much stronger than outside the profile (rho -0.083, 5,849 bars). It shows on both sides. After the largest down days (bottom quintile) the next day is +0.32 of a usual move (t 5.59, 237 bars, t per bar). After up days in the fourth quintile it is -0.145 of a usual move (t -2.92, 221 bars). After the very largest up days it is only -0.04 (t -0.55, 168 bars).
- **F2:** The brief's own situation, a 3-day rise scaled by the 30-day swing, is followed by a move back over the next 3 days inside the profile. On the 3-day grid the Spearman rho is -0.145 (p 0.006, 362 cases), and the top quintile of 3-day rises gives -0.163 of a usual 3-day move (t -1.70, 54 cases). Outside the profile the same measure has the opposite sign (rho +0.085, p < 0.001, 1,899 cases), and its top quintile continues at +0.296 (t 4.51, 398 cases).
- **F3:** Among the tested idea's active bars, the next-day fall sits almost entirely in the deepest quartile of the forecast: -0.43 of a usual move (t -3.97, 83 cases). The other three quartiles give +0.06 (t 0.63), -0.17 (t -2.15) and +0.01 (t 0.08). The grading is a step at the deepest falls, not a slope.
- **F4:** Within the profile, an up day that closes in the top third of a wide day's range is followed by a fall: -0.232 of a usual move (t -2.19, 86 bars). A day that closes mid-range on a middling range is followed by -0.304 (t -3.56, 97 bars). A wide day closing in its bottom third rebounds +0.393 (t 4.57, 129 bars), which repeats the long rebound ideas the map already lists in falling agitated.
- **F5:** The tested book's edge fades over time. The next-day scaled move on active bars is -0.28 in 2018 (t -2.42, 93 cases), -0.14 in 2019 (t -1.69), -0.01 in 2020 (t -0.18) and -0.08 in 2021 (t -0.75). Two windows, w14 (+0.089) and w18 (+0.068), carry about 60 % of the summed daily book return over w7 to w18 (about +0.25).
- **F6:** Other angles did not stand out once the number of angles looked at is counted. Within the profile, Tuesday gives +0.27 (t 3.66) and Saturday +0.14 (t 2.91), with no reason behind either; no idea is drawn from them.

## Ideas
- `058-01.g2.g1.d1.d1.g1_agitated-decline-rally-give-back` (from F2, F1): In a falling, agitated market, a coin's rise over the past 3 days is partly given back over the next 3 days, and the larger that 3-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall that follows.
- `058-01.g2.g1.d1.d1.g2_agitated-decline-up-day-reverses` (from F1, F4): In a falling, agitated market, a coin's up day is followed by a fall over the next day, and the larger the up day against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
