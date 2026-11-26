---
line: 7.g patterns
backtest: 058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d
idea tested: 058-01.g2.g1.d1_bounce-in-decline-wick-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4470 USD
---
## Findings
- **F1:** In the falling agitated profile (15.5 % of coin-days in folds B, C), an up day is followed by a fall the next day: the mean excess next-day return is −0.98 % (t −2.54, 613 cases on 258 days). Outside the profile up days are flat (−0.14 %, t −0.89, 3,572 cases), so the effect belongs to this profile, as the brief says.
- **F2:** The tested condition "3-day return still negative" adds nothing in folds B, C. Up days with a negative 3-day return fall −0.99 % the next day (t −1.52, 236 cases). Up days with a positive 3-day return fall −0.95 % (t −2.24, 370 cases on 167 days). The idea's restriction drops about 60 % of the cases.
- **F3:** Among up days in the profile, the next-day fall grows with how far the close sits below the day's high, in 30-day daily standard deviations. By quartile of that depth (0.07, 0.21, 0.39, 0.81), the next-day excess returns are −0.47 %, −0.55 %, −0.73 % and −1.67 % (t of the top quartile −1.80, 136 cases).
- **F4:** Among the tested book's cases (up days inside a falling 3-day move), the deeper the 3-day fall was in usual swings, the larger the next-day fall. By third of the 3-day z-score (−1.09, −0.39, −0.10), the next-day excess returns are −2.16 % (t −2.12, 68 cases, 38 days), −0.70 % and +0.78 %.
- **F5:** The brief's own grading does not show. Among profile days with a positive 3-day return, the next-day excess return by quartile of the 3-day rise in usual swings is +0.21 %, +0.07 %, −1.49 % and +0.11 %. Over 2 days it is +1.38 %, +1.26 %, −2.09 % and +0.32 %, so the largest rises are not the ones given back most.
- **F6:** The up-day fall holds across coins and years. It is negative on all six coins, with t ≤ −2 on BTC (−1.08 %), LTC, XMR and ZEC, and negative in all four years (2018 −1.45 %, 2019 −1.39 %, 2020 −0.32 %, 2021 −0.85 %).
- **F7:** Down days in the profile rebound the next day: +1.26 %, t 3.15, 675 cases on 289 days. The rebound is graded by the day's fall in usual swings: the lowest fifth (z −1.33) gains +2.18 % (t 2.92). This is already held: the map lists 12 long falling agitated rebound strategies, so it is no discovery.
- **F8:** The book's gain rests on a few days. Its 10 best days sum to +12.8 % of daily return, more than its total of +10.9 % over 1,449 days, and its 10 worst days sum to −6.3 %. This fits a book in a position on only 4 % of coin-days.

## Ideas
- `058-01.g2.g1.d1.g1_agitated-decline-up-day-fade` (from F1, F2, F3, F6): In a falling, agitated market, a coin's up day is followed by a fall over the next day. The further the day closed below its high, measured against the standard deviation of its daily returns over the past 30 days, the larger that next-day fall.
- `058-01.g2.g1.d1.g2_bounce-after-deep-fall-fails` (from F4, F1): In a falling, agitated market, an up day that comes after a fall over the past 3 days is followed by a fall over the next day. The deeper that 3-day fall, measured against the standard deviation of the coin's daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
