---
line: 7.g patterns
backtest: 031-02_extreme-fall-partly-rebounds_1d
idea tested: 031-02_extreme-fall-partly-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3695 USD
---
## Findings
- **F1:** The tested situation adds nothing at the grid level. The 52 in-regime 30-day cases have a mean excess return of +0.02 %, against −0.003 % for the 462 out-of-regime cases. At the 30-day horizon, the coin's past 90-day return quintiles show no lean: bottom quintile −3.9 %, top quintile −3.5 %, Welch t 0.05, Spearman rho 0.062 (p 0.54) over 103 cases.
- **F2:** The book's trades do not grow with the depth of the fall. By tercile of entry forecast, mean net trade profit is +10.9 % in the lowest tercile, +4.6 % in the middle and +5.7 % in the highest (80 trades each). The highest tercile's median is −1.7 %, against +3.3 % for the lowest.
- **F3:** The book's gain sits in a few coins and a few large trades. XRP's 35 trades average +30.8 % against a median of +2.3 %. BTC's 11 trades average −5.4 % and ETH's 34 trades average −1.2 %.
- **F4:** The strongest pattern was short-term continuation, and it is not reliable. The coin's 14-day return, scaled by its 60-day volatility, predicts the next 7 days with a slope of +0.087 usual moves per unit, but the day-clustered t is only 1.45 (1094 cases, 211 days). Its top-minus-bottom quintile spread (+3.0 % against −1.6 %) and the 7-day Welch t of 3.65 count cases from the same day separately.
- **F5:** That continuation does not hold across the data. By coin, its slope runs from −0.007 (LTC, t −0.10) to +0.215 (XRP, t 2.33). By year, it is negative in 2018, 2019 and 2023. It does not separate by side: t +0.72 after rises, −0.62 after falls.
- **F6:** The weekday pattern is weak. On the per-day mean over coins, Saturdays' excess return is +0.33 % (t 2.21, 414 days), positive in 6 of 8 years. Thursdays' is −0.31 % (t −1.39). Among 7 weekdays this is not beyond chance.
- **F7:** At the 30-day horizon, no other angle reached a day-clustered quintile t above 1.1 among the eleven looked at (past 7- to 90-day returns, 20-day volatility, volatility ratio, volume ratio, 30-day drawdown, 30-day range position, last day's return). The volatility-ratio rank correlation was −0.122 (p 0.018). This is unremarkable among 22 feature-horizon tests.

## Ideas
- No ideas: Over about 30 angles (eleven features at two horizons, slopes at three horizons, coins, years, volatility halves, weekdays and trades), no pattern stood out beyond chance. The best candidate, 14-day continuation over the next 7 days, has a day-clustered t of only 1.45 and flips sign across coins and years, and the Saturday effect (t 2.2) is one of seven weekdays tested.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
