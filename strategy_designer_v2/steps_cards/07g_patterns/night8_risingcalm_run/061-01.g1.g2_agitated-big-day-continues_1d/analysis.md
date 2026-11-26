---
line: 7.g patterns
backtest: 061-01.g1.g2_agitated-big-day-continues_1d
idea tested: 061-01.g1.g2_agitated-big-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3748 USD
---
## Findings
- **F1:** In calm markets the effect points the way the brief says and the agitated test does not: on the 5-day grid, the slope of the coin's demeaned 5-day return on the day's move in 30-day swing units is +1.48 % per swing unit (t 2.52, 744 cases on 187 days) in calm markets, against +0.54 % (t 0.58, 551 cases on 165 days) in agitated ones.
- **F2:** The calm-market follow-through is graded in the 5-day bucket means: days above +2 swings are followed by +6.34 % (t 1.75, 28 cases), +1 to +2 swings by +2.59 % (t 1.73, 68), 0 to +1 by +0.91 %, 0 to -1 by -0.89 %, -1 to -2 by -1.09 % and below -2 swings by -3.39 % (t -1.03, 17).
- **F3:** The calm-market slope is not carried by one period or one coin: it is positive in all four years (2018 +0.33 % t 0.29, 2019 +1.82 % t 2.03, 2020 +1.10 % t 0.84, 2021 +1.65 % t 2.04), in 9 of 12 windows (mean +1.08 %), and in 5 of 6 coins (LTC +1.55 % t 2.57, XMR +1.89 % t 2.74, BTC +0.85 % t 1.66; ZEC -0.04 % t -0.04).
- **F4:** Inside calm markets the effect is strongest when the 60-day trend is flat: the slope is +2.77 % per swing unit (t 2.70, 101 cases on 55 days) in choppy calm, against +2.49 % (t 2.10, 178) in rising calm and +1.26 % (t 1.23, 219) in falling calm.
- **F5:** Calm big days (beyond 1.5 swings) are followed by a 5-day move in their own direction of +3 to +7 % in every trend tested (choppy +5.11 % t 2.87, rising +7.00 % t 2.27, falling +3.95 % t 1.52). The up days carry more of it (+4.83 % t 2.16, 46 cases) than the down days (+2.85 % t 1.46, 40 cases). That per-case move is more than 15 times the 0.19 % cost of a trade.
- **F6:** The calm follow-through shows only past 3 days: the slope is -0.14 % at 1 day (t -1.15), about 0 at 2 and 3 days (t -0.16, -0.05), +1.48 % at 5 days (t 2.52) and +1.87 % at 10 days (t 1.74). The move builds over a week rather than starting at once, so the horizon has to be 5 days or more.
- **F7:** In agitated markets the next day reverses rather than continues: the 1-day slope is -0.50 % per swing unit (t -2.00, 2906 cases), and days below -2 swings are followed by +4.38 % the next day (t 2.50, 60 cases). This is the agitated fall rebound the profile map already holds 10 to 12 times, so it is not a discovery; it explains why the tested agitated book lost money (Sharpe -0.04, unusual move -0.49 % per case).

## Ideas
- `061-01.g1.g2.g1_calm-big-day-continues` (from F1, F2, F3, F5, F6): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving in that day's direction over the next 5 days.
- `061-01.g1.g2.g2_choppy-calm-day-follow-through` (from F4, F5, F1): In a choppy, calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving in that day's direction over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
