---
line: 7.b inconclusive
backtest: 032-03.b1_deep-low-rebound-all-coins_1d
idea tested: 032-03.b1_deep-low-rebound-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4034 USD
---
## Findings
- **F1:** The rebound shows over the first 1 to 3 days after the new 30-day low and has faded by the plan's 5 days: on the 160 cases of folds B and C, with cases of the same day pooled (83 days), the mean unusual move is +1.96 % at 1 day (t 1.58), +1.97 % at 2 days (t 1.65), +2.61 % at 3 days (t 2.22) and only +1.54 % at 5 days (t 0.87). Without pooling, it is +0.79 % at 10 days (t 0.55) and −0.49 % at 20 days (t −0.23). The plan measured the idea at a horizon past its peak, which matches the verdict's 5-day +0.54 % with t 0.64.
- **F2:** The grading holds when the fall is measured against the coin's own usual moves, as the forecast does, and fails on the raw fall. By forecast tercile, the pooled 5-day unusual move rises from −1.15 % (t −0.57) through +1.71 % (t 0.49) to +4.17 % (t 2.24, 38 days), and the top tercile's 3-day move is +4.20 % (t 2.57). By the raw 30-day return, the deepest third falls further: −3.78 % at 5 days (t −1.58) and −10.6 % at 10 days (t −4.05, unpooled).
- **F3:** The same grading shows with the 30-day fall in units of the coin's 30-day mean daily range. The top third gains +4.65 % over 3 days (t 1.97, 23 days), the middle third +3.94 % (t 1.41) and the bottom third +0.43 % (t 0.17).
- **F4:** The effect is mixed across periods. In 2018 the high-forecast cases lose −4.26 % over 5 days (t −0.91, 11 cases), while 2019 gains +6.97 % (t 1.80) and 2021 gains +5.97 % (t 2.58, 34 cases). By coin, the 5-day move is positive in BTC (+1.6 %), XMR (+5.3 %) and ZEC (+4.3 %) and negative in ETH (−1.0 %) and XRP (−2.9 %). This spread drowns the pooled mean at 5 days.
- **F5:** A large fall on the low's own day is followed by a sharp but short bounce. In the third of cases with the largest last-day fall, measured in units of the 30-day mean range, the move is +4.76 % at 1 day (t 1.77) and +3.62 % at 2 days (t 2.17, 22 days), and it is gone by 5 days (−0.20 %, t −0.05). The correlation of that fall with the 1-day move is 0.42, against 0.05 with the 5-day move.
- **F6:** Wider recent swings go with a larger 5-day rebound. The top third of the 30-day mean daily range gains +4.97 % over 5 days (t 2.42, 30 days), against −0.91 % (t −0.39) for the bottom third.

## Ideas
- `032-03.b1.b1_three-day-rebound-after-volatile-low` (from F1, F2, F3, F4): In a coin whose daily high-low ranges over the past 30 days are wide compared with its own past year, a close at a new 30-day low is followed by a rise over the next 3 days. The larger the coin's 30-day fall into that low compared with its own usual 30-day moves, the larger the rise.
- `032-03.b1.b2_capitulation-day-short-bounce` (from F5, F1): In a coin whose daily high-low ranges over the past 30 days are wide compared with its own past year, a close at a new 30-day low is followed by a rise over the next 2 days. The larger that day's fall compared with the coin's mean daily range over the past 30 days, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
