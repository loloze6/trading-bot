---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound
line: 7.b inconclusive
backtest: 027-01_panic-range-multiple-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 24 hours, and the larger that range multiple, the higher the return.
Consequence: The panic discount is paid back within about a day rather than over two weeks, so a trader would buy the most intense panics for a one-day hold and not keep the position for weeks.
Why:
- F1: The effect shows only over the first day: on the same cases at 6 bars (24 hours), the mean unusual move is +0.55 % (t 3.60, 1,291 cases, strength 0.109), but it fades to +0.33 % at 18 bars (t 1.38), and is about zero at 42 bars (t -0.06) and at the plan's 84 bars (+0.005 %, t 0.01, strength -0.0005).
- F2: With one case per 6-bar grid cell, the 24-hour unusual move is +0.24 % (t 4.69, 9,979 cases, strength 0.049, total move +0.38 %); the effect is weaker over 12 hours (+0.12 %, t 3.84, 14,550 cases) and over 48 hours (+0.19 %, t 2.17, 6,548 cases).
- F3: The 24-hour move grows with the panic reading: by quintile of the raw component (mean reading 0.36, 0.62, 0.94, 1.58, 5.77), the unusual move is -0.10 % (t -0.98), -0.16 % (t -1.52), +0.22 % (t 2.08), +0.31 % (t 2.62) and +0.91 % (t 7.09), with a Spearman correlation of 0.092 between the reading and the move.
- F4: The 24-hour effect is broad: it is positive in all six coins (from +0.09 % in BTC, t 1.09, to +0.36 % in XMR, t 3.03) and in seven of eight years (t from 2.07 to 3.90 in 2019, 2020, 2021 and 2024; 2018 is -0.02 %).
- F5: At 84 bars the market's own moves drown the effect. The yearly means swing from -9.7 % in 2018 (t -6.10) and -3.4 % in 2022 (t -2.52) to +4.5 % in 2020 (t 2.32), the coins all sit between -0.46 % and +0.47 % with |t| < 0.43, and no forecast quintile has |t| above 1.34.
- F8: Against cost, the 24-hour total move of +0.38 % per case (F2) is about 2 times the 0.19 % cost of a trade, and the top quintile's +0.91 % unusual move (F3) is about 4.8 times that cost.
