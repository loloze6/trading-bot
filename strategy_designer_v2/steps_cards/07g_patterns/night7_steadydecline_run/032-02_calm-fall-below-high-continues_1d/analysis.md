---
line: 7.g patterns
backtest: 032-02_calm-fall-below-high-continues_1d
idea tested: 032-02_calm-fall-below-high-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4420 USD
---
## Findings
- **F1:** In the falling calm profile, the coin's past return predicts the next 3 days' unusual move in the same direction (continuation), and the 14-day return does so most surely: slope 0.087, t 2.40 on 559 grid cases; the 7-day return gives 0.124 (t 2.07, 582 cases) and the 3-day return 0.182 (t 2.03, 613 cases). The tested depth below the 30-day high gives only 0.043 (t 1.02, 502 cases).
- **F2:** Depth below the 30-day high does not grade the move in the falling calm profile. Its quintiles from shallowest to deepest give unusual 3-day moves of -1.27 %, -1.80 % (t -2.14), +0.64 %, +0.60 % and -0.18 %. The 7-day return's quintiles run nearly in order: -2.35 % (t -1.96, 146 cases), -1.18 %, +0.37 %, +0.18 %, +2.11 %.
- **F3:** Outside the calm case, the continuation turns into reversal. In falling non-calm grid cases, past returns slope negatively on the next 3 days (r7 -0.088, t -0.91; r3 -0.110, t -0.88; 242 cases). The next day's unusual return slopes on today's return at -0.175 (t -2.79, 1,902 bars) over all falling bars, against -0.035 (t -0.76) in falling calm alone. Over all bars the slope is -0.087 (t -2.87, 8,262 bars), and the lowest decile of one-day returns is followed by +0.95 % the next day (t 2.16, 276 days).
- **F4:** The falling-calm continuation is unstable across years and coins. In 2018 the r7 slope is 0.163 (t 1.88), against -0.025 in 2019 and -0.125 in 2020. ETH (t 2.30) and LTC (t 1.96) carry it, while BTC is flat (-0.015, t -0.22). Mean unusual 3-day moves of falling calm grid bars are negative in 2018 and 2019 (-1.24 %, -1.33 %) and positive in 2020 and 2021 (+2.65 %, t 2.25; +2.33 %, t 2.02).
- **F5:** The book earns from long stretches of decline, not from 3-day holds. Trades of up to 3.5 days lose -3.66 % on average (209 trades), and trades of 3.5 to 7 days lose -3.35 % (145). Trades over 15 days gain +7.78 % (162). The book's daily returns correlate at -0.47 with the coins, and its best 5 % of days come on days the coins fell -6.8 % on average.
- **F6:** Cost is not what keeps the book from paying. The tested idea's unusual move per case, +1.06 % (t 2.60), is 5.5 times the 0.19 % trade cost. The book fails because the depth forecast misgrades the cases (F2): its slope t is 1.22.

## Ideas
- `032-02.g1_calm-decline-fourteen-day-continuation` (from F1, F2, F6): In a falling, calm market, the more a coin has fallen over the past 14 days, the more it falls over the next three days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-02.g2_agitated-fall-next-day-rebound` (from F3): In a falling, agitated market, the larger a coin's one-day fall, the more it rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
