---
line: 7.g patterns
backtest: 032-01_calm-decline-depth-continues_1d
idea tested: 032-01_calm-decline-depth-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3877 USD
---
## Findings
- **F1:** Across the coins, the next day's excess return falls as the day's standardised return rises (the day's return over its 20-day standard deviation, clipped at ±4): the slope is negative in 5 of 6 coins, with t -2.07 (BTC), -2.48 (ETH), -2.00 (LTC), -3.84 (XMR) and -1.82 (ZEC), against +0.26 for XRP (928 to 1113 bars each).
- **F2:** Days in the lowest sextile of the standardised day return (mean z -1.58) are followed by a next-day excess return of +0.76 % (t 2.34, 366 days), while the middle sextiles sit between -0.40 % and +0.07 %. The rebound is still +1.11 % over 2 days (t 1.80, 180 days) and has faded by 3 days (+0.38 %, t 0.42); each of these is 4 to 6 times the 0.19 % cost of a trade.
- **F3:** Large down days (z below -1.5) on volume above the coin's median, against its 28-day mean, are followed by a next-day excess return of +1.20 % (t 2.13, 136 days); the same days on low volume are followed by -0.10 % (t -0.12, 36 days).
- **F4:** The rebound after days with z below -1.5 is positive in all 6 coins (+0.39 % to +1.55 %; t 2.42 for LTC and 2.47 for XMR) and in all 4 years (+0.38 % to +1.82 %).
- **F5:** The tested situation is rare and not graded: calm bars are 6.9 % of all bars. Across the calm 28-day-return terciles (-23.6 %, +0.6 %, +32.6 %), the 5-day excess returns are -0.04 % (t -0.02), -0.26 % (t -0.09) and +3.72 % (t 1.10), so deeper calm falls are not followed by larger further falls.
- **F6:** Outside calm bars, the 28-day return does not grade the next 5 days either: the 5-day excess return is -0.64 % (t -0.37) in the deepest-fall quintile and +0.62 % (t 0.59) in the highest-rise quintile.

## Ideas
- `032-01.g1_sharp-daily-fall-rebounds` (from F1, F2, F4): When a coin's daily return is a fall that is large against its own typical daily move over the past 20 days, the coin rises over the next 1 to 2 days, and the larger that fall in units of its typical daily move, the larger the rise.
- `032-01.g2_high-volume-selloff-day-rebounds` (from F3, F2): When a coin falls sharply in one day on volume that is high against its own 28-day average, it rises over the next day, and the higher that day's volume relative to its average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
