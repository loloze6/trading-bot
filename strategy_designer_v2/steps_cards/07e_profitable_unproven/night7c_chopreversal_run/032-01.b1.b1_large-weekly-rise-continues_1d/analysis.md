---
line: 7.e profitable but not proven
backtest: 032-01.b1.b1_large-weekly-rise-continues_1d
idea tested: 032-01.b1.b1_large-weekly-rise-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3784 USD
---
## Findings
- **F1:** The book's gain is not mainly the market's own rise: summed over coins and windows, the position's gain before costs is 3.07 against 0.95 from the market's own rise (about 31 %), so about 2.1 is timing.
- **F2:** The gain sits in two windows. w10 earns +1.42 and w17 earns +1.13 of the book's summed daily returns, together 2.55 of 2.94. w9 loses 0.88 and w12 loses 0.36.
- **F3:** The gain also sits in three coins and a few trades. XRP earns +1.06, ETH +0.79 and BTC +0.71, while LTC loses 0.05 and ZEC earns only +0.04. The top 5 of 259 trades carry 572 of 1475 summed net trade percent (39 %), and the top 10 carry 861 (58 %). The median trade is +2.15 %, with 60 % winners.
- **F4:** On all non-overlapping 7-day grid bars, the next 7-day unusual move rises steadily with the 7-day return scaled by the 30-day daily swing (z), on both sides:
- **F5:** The continuation lives in choppy, low-efficiency markets, the opposite of the brief's reversal. Split by terciles of the 30-day efficiency ratio (net move over the summed absolute daily moves), the slope of the next 7-day unusual move on z is:
- **F6:** After a z ≥ 1 weekly rise, the next 7-day unusual move is +3.42 % (t 2.05, n 125) when the 30-day return is positive, against +1.54 % (t 0.49, n 33) when it is negative.
- **F7:** After a z ≥ 1 rise, the next 7-day unusual move is larger when the coin's 30-day daily swing is in its calmest tercile: +4.79 % (t 1.90, n 60), against +2.22 % (n 46) in the middle tercile and +1.72 % (n 52) in the most agitated.
- **F8:** The slope of the next 7-day unusual move on z is positive in all 6 coins, from 0.0056 (ZEC) to 0.0372 (XRP). From the book's entry bars, the unusual move is +1.20 % over 3 days (t 1.41, n 154), +0.87 % over 7 days (t 0.58, n 151) and −3.36 % over 21 days (t −1.45, n 120).

## Ideas
- `032-01.b1.b1.e1_large-weekly-fall-continues` (from F4, F8): When a coin has fallen over the past 7 days by a large amount compared with its typical daily swing over the past 30 days, it tends to keep falling over the next 7 days. The larger that 7-day fall counted in 30-day daily swings, the larger the further fall.
- `032-01.b1.b1.e2_choppy-market-weekly-move-continues` (from F5, F4, F1): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days. The larger that scaled 7-day move, the larger the following move.
- `032-01.b1.b1.e3_weekly-rise-within-rising-month` (from F6, F4, F2): When a coin's 30-day return is up and it has risen over the past 7 days by a large amount compared with its 30-day daily swing, it tends to keep rising over the next 7 days. The larger that scaled 7-day rise, the larger the further rise.
- `032-01.b1.b1.e4_calm-month-weekly-breakout-continues` (from F7, F4): When a coin's daily swings over the past 30 days are small compared with its usual swings, a 7-day rise that is large counted in those swings tends to be followed by a further rise over the next 7 days. The calmer the past 30 days, the larger that further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
