---
line: 7.g patterns
backtest: 032-01_flat-range-upside-break-fades_1d
idea tested: 032-01_flat-range-upside-break-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4579 USD
---
## Findings
- **F1:** After a daily fall, the next day's move against the coin's drift is a rebound, and the larger the fall the larger the rebound. Days falling more than 1× their 20-day volatility were followed by a mean unusual next-day move of +0.89 % (t 2.35, cases summed per day; 922 cases on 281 days; strength 0.16). That is about 4.7 times the 0.19 % cost of a trade. The rebound was positive in 11 of 12 windows (w9 alone −0.97 %) and in all six coins (BTC +0.38 % up to XMR +1.28 %, t 3.06).
- **F2:** The rebound is graded by the size of the day's move in volatility units. The Spearman correlation between the day's return over its 20-day volatility and the next day's unusual move is negative in every coin (ρ −0.08 to −0.14, all p < 0.007). The mean next day after a fall rises from +0.26 % (z in −1..0) to +0.88 % (z in −2..−1, t 4.1) to +1.55 % (z ≤ −2, t 3.2).
- **F3:** The rebound is lopsided. After rises the next day shows little or no giving back: −0.23 % for z in 0..1, +0.09 % for z in 1..2 and +0.03 % for z > 2, with t between −2.4 and +0.4. The reversal effect sits mostly after falls.
- **F4:** In folds B and C, 60-day upside breakouts in trendless coins (efficiency ratio ≤ 0.3) kept rising instead of fading. The 10-day unusual move was +9.8 % (t 2.28; 62 cases on 42 days; hit rate 58 %), and over 5 days it was +5.2 % (t 2.35, 80 cases). This matches the verdict's short-side −4.35 % (t −1.97, 136 cases).
- **F5:** That breakout continuation is not graded and not broad, so it supports no idea. By overshoot tercile it ran +18.9 %, −4.4 %, +14.3 %, and by efficiency-ratio tercile +8.9 %, +10.7 %, +9.9 %. It also rests on few coins and windows: XRP +48.6 % and w17 +32 %, while BTC was −4.9 %.
- **F6:** Some weekday means stand out, but none is graded. Friday's daily return averaged +0.55 % (t 3.47, n 1050) and Thursday's −0.43 % (t −2.28, n 1050). Across seven weekdays, only Friday clearly stands apart from chance.

## Ideas
- `032-01.g1_next-day-rebound-after-falls` (from F1, F2, F3): In a coin that has just closed a day with a fall, the next day's return is above the coin's normal drift, and the larger that day's fall measured against its 20-day volatility, the larger the rebound over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
