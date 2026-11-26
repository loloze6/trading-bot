---
line: 7.g patterns
backtest: 060-01.g1.d2.d2_wider-squeeze-day-fades-harder_1d
idea tested: 060-01.g1.d2.d2_wider-squeeze-day-fades-harder
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5330 USD
---
## Findings
- **F1:** In the falling agitated profile, the next day after an up day of ordinary size is weak. When the day's return is between 0 and 1 of its 20-day swing, the next-day unusual move is -1.18 % (t -2.71, 431 cases). When it is between 0.5 and 1 swing, it is -1.72 % (t -3.71, 154 cases) and -2.28 % over two days (t -2.87, 152 cases). After larger up days, from 1 to 2 swings, it is +0.65 % and +0.62 % (t 0.83 and 0.27), which cannot be told from 0.
- **F2:** The weak next day after a small up day in the falling agitated profile holds across the sample. It is negative on all 6 coins, from -0.70 % to -1.57 % (BTC t -2.26, LTC t -2.62). It is negative in 3 of 4 years (2018 -2.24 %, t -2.53; 2019 -0.82 %; 2021 -1.73 %), and flat in 2020 (+0.01 %).
- **F3:** Outside the falling agitated profile, a coin whose 20-day return lies between -10 % and -20 % has a next-day unusual move of -0.67 % (t -2.89, 809 cases). In the falling calm profile alone the same stretch gives -1.20 % (t -3.20, 278 cases).
- **F4:** This continuation is not graded at its deep end. In the falling calm profile a 20-day fall deeper than 20 % gives only -0.30 % (t -0.67, 341 cases).
- **F5:** The continuation in F3 appears on all 6 coins: LTC -1.22 % (t -3.26), ETH -0.84 % (t -2.36), BTC -0.80 % (t -1.86), XRP, XMR and ZEC from -0.23 % to -0.50 %. It is negative in 3 of 4 years (2018 -1.39 %, t -3.26) and positive in 2021 (+0.39 %). The falling calm short cell of the map holds only one strategy (035-01.b1).
- **F6:** The brief's grading by close location is not in the falling agitated bars. Closes from 0.6 to 0.8 of the range give -0.84 % (t -1.82), closes from 0.8 to 1 give -0.49 % (t -0.76), and closes above 0.9 give -0.22 % (t -0.24).
- **F7:** The tested grading by range ratio rests mostly on its widest days. High closes on days whose range is above 1.6 times the 20-day mean give -2.69 % (t -2.14, 41 cases). Ratios from 0.9 to 1.6 give -0.67 % (t under 0.8), which is why the main t stops at 1.83.
- **F8:** In the falling agitated profile, low closes (under 0.2 of the range) are followed by +2.17 % (t 2.85, 243 cases). Low closes rebound more the wider the day: +1.92 % at range ratio 0.9 to 1.2, +2.01 % at 1.2 to 1.6 and +3.95 % above 1.6. This effect is already held by the map (039-02, 045-01, 044-01) and is left out as a discovery.
- **F9:** On the book's best 2 % of days the coins fall 6.6 % on average, and on its worst 2 % of days they rise 7.1 %. The book is a pure bet on the next-day direction of its shorts, with a daily standard deviation of 0.32 %.

## Ideas
- `060-01.g1.d2.d2.g1_agitated-downtrend-up-day-fades` (from F1, F2, F6): In a falling, agitated market, a coin that closes a day up falls back over the next two days. The larger that day's rise against the coin's average daily swing of the last 20 days, the larger the fall.
- `060-01.g1.d2.d2.g2_calm-downtrend-fall-continuation` (from F3, F4, F5): In a falling, calm market, a coin that has fallen over its last 20 days keeps falling over the next day. The larger its 20-day fall against its average daily swing over those 20 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
