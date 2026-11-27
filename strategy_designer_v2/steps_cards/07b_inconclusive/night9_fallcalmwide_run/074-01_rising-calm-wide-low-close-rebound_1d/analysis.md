---
line: 7.b inconclusive
backtest: 074-01_rising-calm-wide-low-close-rebound_1d
idea tested: 074-01_rising-calm-wide-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3705 USD
---
## Findings
- **F1:** In the folds shown (B, C), the rebound depends on how near the close sits to the day's low, not on how wide the day is. Cases in the tercile closing nearest the low (mean position 0.92 of the range from the high) earn +3.37 % excess the next day (t 5.48, 44 cases). The middle tercile earns +1.91 % (t 2.11), and the tercile farthest from the low earns +0.40 % (t 0.30).
- **F2:** The tested forecast grades on the wrong thing. It multiplies width by nearness to the low, and that product has no link to the next-day excess return (Pearson −0.013, Spearman 0.004, 132 cases). Width alone has none either (Pearson 0.006, n 107), and the widest quarter of days (4.0 swings) earns +1.39 % (t 1.35), less than the third quarter's +2.10 % (t 2.94). Nearness to the low carries the link (Pearson 0.195, t 2.27). So the step-5 correlation of 0.10 and t of 1.93 mix a graded part of the signal with a part that adds only noise.
- **F3:** The rebound lasts and grows past one day. Pooled excess is +1.89 % at 1 day (t 2.82), +2.74 % at 2 days (t 3.02), +3.75 % at 3 days (t 3.26) and +3.66 % at 5 days (t 2.96), on 132 cases.
- **F4:** Over 3 days, the nearest-to-low tercile earns +5.76 % (t 4.42). The distance from the close to the low, measured in swings, correlates −0.257 with the 3-day excess (t −2.73, n 107), so a closer low close gives a larger 3-day rise.
- **F5:** The effect is broad across coins over 3 days but uneven by period. Every coin with enough cases except XRP is positive over 3 days (XMR +4.88 % t 3.57, LTC +5.32 % t 2.65, TRX +4.82 % t 3.50; XRP −0.01 %). By year, the 1-day excess is clear in 2018 (t 2.98) and 2021 (t 2.89) but small in 2019 (t 0.71) and 2020 (t 0.66).
- **F6:** No more data is available, because the test already used all four folds and all 19 coins on daily bars. The step-5 t of 1.93 is lower than this exploration's 2.82, which means folds A and D are weaker. Rerunning the same idea on the same data cannot settle it.

## Ideas
- `074-01.b1_low-close-nearness-rebound` (from F1, F2, F6): In a rising, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes near its low is followed by a rise over the next day; the nearer the close to the day's low, the larger the rise.
- `074-01.b2_three-day-low-close-rebound` (from F3, F4, F5, F2): In a rising, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes near its low is followed by a rise over the next three days; the nearer the close to the day's low, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
