---
line: 7.g patterns
backtest: 032-03.b1.b1_thin-volume-decline-all-coins_1d
idea tested: 032-03.b1.b1_thin-volume-decline-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3910 USD
---
## Findings
- **F1:** Among coins that rose over the past 28 days, the lower their 28-day mean volume against the 60 days before, the higher the next 5 days' excess return (Spearman rho -0.27, p 2e-6, 294 non-overlapping cases in windows w7 to w18). The thinnest-volume quintile (log ratio about -0.76) gained +14.4 % (day-clustered t 2.07), the next quintile +3.9 % (t 1.65), and the heaviest-volume quintile -1.3 % (t -0.63); the top-quintile mean is likely carried by a few large moves.
- **F2:** Across all bars, a higher 28-day return is followed by a higher 5-day excess return (rho 0.073, p 0.002, 1706 cases). By quintile this rises from -1.4 % and -1.7 % (t -1.69) in the two most negative to +1.0 % and +2.2 % in the two most positive.
- **F3:** Inside declines the tested relation is absent: excess 5-day return on the 28-day volume ratio has rho 0.085, p 0.17, 260 cases, with quintile means of -1.4 %, -4.0 %, -2.0 %, +1.7 % and +0.0 %. This matches step 5's slope t of 1.03 and an unusual move of +0.21 % per case (t 0.73), which is 0.9 times the 0.22 % cost of a trade.
- **F4:** The 28-day range contraction shows a strong pooled link (rho -0.17, p 4e-5; lowest quintile +10.8 %, t 2.65), but it is not stable and is not a finding: its sign flips across windows (rho +0.59 in w7, +0.43 in w12, -0.41 in w18, -0.43 in w8), and its 14-day version is null (rho -0.04, p 0.13).
- **F5:** Coins in a 28-day decline had a negative mean excess 5-day return in every year shown (2018 -1.1 %, 2019 -1.5 %, 2020 -0.4 %, 2021 -1.4 %). Coins in a 28-day rise had a positive one in 2020 (+1.2 %) and 2021 (+2.4 %).
- **F6:** The book stayed close to flat while holding was far ahead: its mean daily return was negative in 5 of 12 windows (w8, w9, w10, w17, w18), and it trailed holding in w10 (-0.10 % vs +0.57 % a day) and w11 (+0.01 % vs +1.90 %).

## Ideas
- `032-03.b1.b1.g1_thin-volume-rise-keeps-rising` (from F1, F5): Among coins that have risen over the past 28 days, the lower the volume over those 28 days compared with the coin's volume in the 60 days before, the larger the further rise over the next 5 days.
- `032-03.b1.b1.g2_four-week-momentum-continues` (from F2, F5, F3): The larger a coin's return over the past 28 days, the larger its return over the next 5 days, rises followed by further rises and falls by further falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
