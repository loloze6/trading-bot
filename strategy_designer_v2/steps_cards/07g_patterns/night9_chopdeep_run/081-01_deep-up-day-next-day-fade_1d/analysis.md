---
line: 7.g patterns
backtest: 081-01_deep-up-day-next-day-fade_1d
idea tested: 081-01_deep-up-day-next-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4524 USD
---
## Findings
- **F1:** On up days the next-day excess return falls steadily as the close sits deeper below the 20-day high in 20-day swings. By depth quintile it runs from −1.14 % (t −5.2, n 727) in the deepest to +0.21 % (t 1.3, n 1696) in the shallowest. On down days the same depth shows no fade: the deepest quintile is +0.48 % (t 1.4) and the shallowest +0.86 % (t 2.7), so the tested asymmetry is in folds B and C.
- **F2:** The up-day depth grade holds whatever the size of the up move. The deep tercile fades −0.81 % (t −3.9), −0.74 % (t −3.6) and −0.87 % (t −3.0) after small, mid and big up days. The shallow tercile is +0.19 %, +0.05 % and +0.27 %.
- **F3:** The fade is graded and largest in falling markets (60-day return below −10 %). Falling agitated runs deep −1.32 % (t −3.3, n 269), mid −0.85 % (t −1.9) and shallow −0.33 %. Falling calm runs deep −0.79 % (t −2.7, n 294), mid −0.65 % (t −2.5) and shallow +0.68 %. Rising markets show no clear grade: in rising agitated the deep tercile is +0.03 % (n 58), and in rising calm only the deep tercile fades (−0.93 %, t −2.2).
- **F4:** The size per case explains why the book does not pay. The pooled unusual move is +0.36 % against a cost of 0.22 %, and the total move of +0.20 % is below that cost. Deep up days in falling markets move −0.8 % to −1.3 % beyond drift (F3), several times the cost, and a falling coin's own drift adds to a short.
- **F5:** The book behaves as a short on the coins. On the book's best tenth of days the coins average −599 bp and the book +242 bp; on its worst tenth the coins average +502 bp and the book −181 bp. Its result depends on market direction, which matches its Sharpe trailing holding's by 0.21.
- **F6:** On down days, heavier volume against the 20-day mean is followed by a larger next-day rebound (Spearman rho 0.09, p 1e-11, n 5594).
- **F7:** Up-day volume does not grade the next day (Spearman rho 0.005, p 0.69). The low-volume up-day fade is in fold C (t_day −2.1) but not in fold B (t_day −1.1). Weekday effects (Monday −0.38 %, t −2.7) and down days closing near their high (−1.47 %, t −2.7, n 135) do not stand out against the number of angles looked at.

## Ideas
- `081-01.g1_falling-deep-up-day-fade` (from F1, F2, F3, F4, F5): In a falling market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
