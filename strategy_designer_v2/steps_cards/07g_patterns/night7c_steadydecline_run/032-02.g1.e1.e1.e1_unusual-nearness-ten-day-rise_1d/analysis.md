---
line: 7.g patterns
backtest: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d
idea tested: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5468 USD
---
## Findings
- **F1:** A coin's one-day fall, measured against its own usual daily move over the 60 prior days, is followed by a next-day rise above the coin's mean. Falls of 2 to 3 usual moves are followed by +2.26 % (124 cases, 58 days, t 3.83). Falls beyond 3 usual moves are followed by +3.00 % (48 cases, 21 days, t 1.12). Falls of 1 to 2 are followed by +0.58 % (611 cases, t 1.36). Falls of 0 to 1 are followed by +0.13 % (t 0.71).
- **F2:** The reversal is graded on the falling side. The fall's size in usual moves times the next day's excess return averages 0.0056 (t 2.24 with the cases of one day summed, 867 days). On the rising side the same product averages only 0.0020 (t 1.18), and rises of more than 2 usual moves are followed by −0.26 %. The effect belongs to falls, not to rises.
- **F3:** The next-day rise after falls of at least 2 usual moves holds in every one of the 12 windows shown, from +0.32 % (w14, 30 cases) to +7.90 % (w13, 7 cases). It also holds in every one of the 6 coins, from +2.22 % (LTC) to +2.91 % (XRP).
- **F4:** The rise after a large fall is about one day long. On non-overlapping 2-day and 3-day grids the graded fall product drops to t 0.39 and t 0.92. On a 5-day grid it is t 1.32, and falls beyond 2 usual moves show +4.22 % over 5 days on only 47 cases.
- **F5:** The rise after a large fall does not depend on the brief's calm or trend condition. After falls of at least 2 usual moves, the next day is +2.07 % when the prior 10 days were calmer than the median and +2.83 % when they were not. It is +2.26 % when the 28-day return was negative and +2.82 % when it was positive.
- **F6:** Per case, the next-day move after a fall of 2 to 3 usual moves (+2.26 %) is about 12 times the 0.19 % a trade cost this backtest.
- **F7:** The tested idea's forecast carries the 10-day effect, and the raw distance from the 28-day closing high adds nothing beyond it. Regressing the 10-day excess return on both gives the forecast a coefficient of 0.074 per 10 points (t 2.43) and the standardised raw distance −0.0014 (t −0.13). By forecast quintile, the top minus the bottom quintile is +2.79 % against −3.46 % (t 3.17, 846 cases).
- **F8:** Among the other angles examined, nothing stood out given how many were looked at. By weekday, the best day was Saturday at +0.58 % (t 2.26), one of seven weekdays tested. Volume ratio showed rho −0.03 (p 0.38) and range ratio rho −0.09 (p 0.03) against the 10-day excess return.

## Ideas
- `032-02.g1.e1.e1.e1.g1_one-day-fall-snaps-back` (from F1, F2, F3, F4, F6): The larger a coin's fall over the last day, measured against its own typical daily move over the past 60 days, the larger its rise over the next day.
- `032-02.g1.e1.e1.e1.g2_sharp-drop-bounces-regardless` (from F1, F5, F3): The larger a coin's fall over the last day, measured against its own typical daily move over the past 60 days, the larger its rise over the next day, and this holds as strongly after calm weeks as after turbulent ones.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
