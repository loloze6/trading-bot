---
line: 7.b inconclusive
backtest: 025-03_bounce-falling-versus-rising-regime_1d
idea tested: 025-03_bounce-falling-versus-rising-regime
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3695 USD
---
## Findings
- **F1:** The tested gap (long cases minus short cases, 5-day excess return) is on the side the idea predicts but small at +0.35 % (Welch t 0.87; 1510 long and 1319 short cases); it grows with the horizon to +0.58 % at 10 days (t 0.92) and +1.65 % at 20 days (t 1.57, 1338 / 1150 cases), and turns negative at 1 day (−0.12 %, t −0.67) and 3 days (−0.30 %, t −0.96).
- **F2:** The effect is mixed across years and drowned by the market's swings. The gap is −3.1 % in 2018 (t −1.77), −2.1 % in 2020 (t −1.78) and −2.8 % in 2022 (t −2.56), against +1.7 % in 2019 (t 1.76) and +2.5 % in 2025 (t 2.46). In falling years both sides lose: in 2022, long −3.6 % (t −3.85) and short −0.8 %.
- **F3:** It is mixed across coins as well, with ETH at +1.5 % (t 1.60), ZEC at +1.2 % (t 0.87) and BTC at +0.75 % (t 1.08), against XRP at −1.7 % (t −1.34) and XMR at −0.27 % (t −0.35).
- **F4:** The test's grading barely separates the cases. 52 % of the cases sit at the forecast cap of 20 (median |forecast| 18.9), while their rise is only 1.6 usual daily moves at the median. The forecast-tercile gaps are flat rather than widening: +0.48 % (t 0.72), +0.45 % (t 0.70) and +0.14 % (t 0.19).
- **F5:** The largest forecasts are followed by small gains in both regimes, +0.55 % for long cases (t 0.95) and +0.41 % for short cases (t 0.84). The tested gap therefore comes mostly from the short side's smaller cases: the low tercile's short cases average −1.21 % (t −2.79).
- **F6:** Measured instead by the rise in usual 20-day moves, the regime gap appears at the largest rises. Above 3 usual moves, the 5-day excess return is +3.38 % in rising coins (t 2.17, n 108) against −0.66 % in falling ones (n 68). Between 2 and 2.5 moves it is +1.08 % against −1.36 % (n 103 / 96). Below 1.5 moves the two regimes are equal (−1.65 % against −1.68 %).
- **F7:** The idea is small against the cost of a trade. Its unusual move is +0.17 % per case (strength 0.017) and its total move is +0.20 %, against a trade cost of 0.19 %. The book's Sharpe is 0.12, against holding's 0.55.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins` (from F1, F2, F3, F6): In one coin, the 5-day return after a one-day rise of several usual daily moves is lower when its 90-day return is negative than when its 90-day return is positive, and the gap widens as the rise gets larger.
- `025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days` (from F1, F4, F6, F7): In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
