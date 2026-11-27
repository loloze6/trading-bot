---
line: 7.g patterns
backtest: 072-02_choppy-deep-up-day-fade_1d
idea tested: 072-02_choppy-deep-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3854 USD
---
## Findings
- **F1:** In a choppy market (60-day return between -10 % and +10 %), on all days and not only up days, the next-day excess return grows more negative with the depth of the close below the 20-day high in 20-day swings, at 0.29 % per unit of depth (t 2.92, 654 coin-days). The deepest fifth (mean depth -5.6) is followed by -1.56 % (t -1.23 over per-day sums). The next three fifths give -0.50 %, -0.56 % and +0.19 %, and the shallowest gives -0.01 %.
- **F2:** The effect is larger over three days than over one. On a non-overlapping 3-day grid in choppy markets, the 3-day excess return falls 0.75 % per unit of depth (t 2.96, 218 cases), about 2.6 times the 1-day slope. A deep close is worth several percent over three days, against a trade cost of 0.19 %.
- **F3:** The deep-close fall in choppy markets does not depend on the day's direction. In the deepest fifth, up days are followed by -1.63 % and down days by -1.51 %. The tested up-days-only restriction kept half the cases and gave a t of only 1.87.
- **F4:** The deepest 40 % of choppy closes are followed by a negative mean excess next day in every year (2018 -1.91 %, 2019 -0.52 %, 2020 -2.38 %, 2021 -0.10 %), in 5 of 6 coins (ZEC +0.32 % is the exception) and in 8 of 12 windows. w16 is the most negative at -10.8 % over 17 cases, so part of the size comes from one window.
- **F5:** The tested book's gain rests on a few days. Its total of 0.166 over 1,449 book-days is less than its 10 best days (+0.242), and its 10 worst days give -0.205. Its 5 positions in w16 average +12.2 % against under 2 % in most other windows.
- **F6:** In falling markets, the larger the day's move in 20-day swings, the lower the next day's excess return, at -0.56 % per unit (t -5.03, 2,063 coin-days). Up days fade: deep up days are followed by -1.04 % and mid-depth up days by -0.80 %. This is the falling-market bounce fade the map already holds (074-01 "graded still down bounce fade", falling, short), so it is not a discovery.
- **F7:** The other angles showed nothing that stands out: no weekday effect (largest |t| 1.21, Wednesday -0.72 %), no graded effect of the day's move within choppy markets (quintile means from +0.06 % to -0.89 %, not monotone), and no depth gradient in rising markets (rank correlation -0.037, p 0.13).

## Ideas
- `072-02.g1_choppy-deep-close-three-days` (from F1, F2, F3, F4): In a choppy market, the further a coin's daily close sits below its 20-day high, measured in units of its 20-day daily-return standard deviation, the larger its fall over the next three days, whether that day closed up or down.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
