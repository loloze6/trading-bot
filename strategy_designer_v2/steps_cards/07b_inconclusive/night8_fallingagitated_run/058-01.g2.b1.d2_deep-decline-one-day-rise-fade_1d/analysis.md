---
line: 7.b inconclusive
backtest: 058-01.g2.b1.d2_deep-decline-one-day-rise-fade_1d
idea tested: 058-01.g2.b1.d2_deep-decline-one-day-rise-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4358 USD
---
## Findings
- **F1:** The fade is real at a one-day horizon and gone by three. On short-bet days in folds B and C, the unusual move over the next day is +0.88 % in the short direction (t 2.24, 714 cases on 280 days; strength 0.16 of the usual 1-day move, t 2.32). Over 2 days it falls to +0.23 % (t 0.27, 147 days), and at the plan's 3-day grid it is +1.00 % (t 1.35, 191 days). So the plan's 3-day horizon diluted a next-day give-back with two days of noise.
- **F2:** The 1-day fade holds across the data rather than in one corner. It is positive on 9 of 10 coins (BTC +0.96 %, t 2.39; ZEC +1.01 %, t 1.93; XMR +0.99 %, t 1.82; only DOGE negative, on 7 cases) and in every year (2018 +1.35 %, 2019 +1.02 %, 2020 +0.42 %, 2021 +0.89 %). It is positive in 9 of 10 windows with more than one case; w11 is negative on 15 cases.
- **F3:** The 60-day fall depth, the idea's second grade, works against it. At 1 day, the deepest-fall quartile of short bets fades only +0.85 % (t 0.80, 40 days) while the shallowest fades +1.36 % (t 3.04, 65 days). At 3 days the quartiles show no order (+1.20 %, +1.92 %, +1.09 %, +1.47 %). The supporting correlation of |forecast| with the move is only 0.02 in step 5, and 0.03 to 0.04 at 1 to 3 days here.
- **F4:** In the profile, the sign and size of the day's move grade the next day's move, up to about one usual swing. Across all profile days, the next-day unusual move in the short direction rises from −3.00 % after days below −1 sd (t −2.37, 68 days), through −0.78 % (−1 to 0 sd), to +0.95 % (0 to 0.5 sd, t 1.86) and +1.17 % (0.5 to 1 sd, t 1.74). Above 1 sd it flattens to +0.17 % (1 to 2 sd) and −0.21 % (above 2 sd). Among rises alone, the Spearman correlation of rise size with the next-day move is −0.0005.
- **F5:** The brief's own situation, a several-day rise, grades the 3-day give-back, but weakly. On profile days on a 3-day grid, the 3-day unusual move in the short direction is −0.35 % after a 3-day rise of 0 to 0.5 usual swings. It is +2.13 % at 0.5 to 1 (t 1.15, 26 days), +2.12 % at 1 to 1.5 (t 0.98, 16 days) and +3.59 % above 1.5 (t 1.17, 10 days). Spearman between the size of the rise and the move is 0.16 (186 rises), and the order is gone at 5 days (−0.11).
- **F6:** The next-day horizon also clears the cost of trading. At 1 day the unusual move per case (+0.88 %) is about 4 times the 0.22 % cost of a trade. At 3 days, after the coins' −0.43 % normal drift in the short direction, the total move is only +0.13 %, 0.6 times that cost.

## Ideas
- `058-01.g2.b1.d2.b1_next-day-fade-of-rises` (from F1, F2, F3, F4, F6): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next day.
- `058-01.g2.b1.d2.b2_multi-day-rally-give-back` (from F5): In a falling, agitated market, the larger a coin's 3-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall in its price over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
