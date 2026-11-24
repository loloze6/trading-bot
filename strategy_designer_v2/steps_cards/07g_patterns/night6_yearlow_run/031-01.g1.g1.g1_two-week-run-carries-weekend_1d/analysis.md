---
line: 7.g patterns
backtest: 031-01.g1.g1.g1_two-week-run-carries-weekend_1d
idea tested: 031-01.g1.g1.g1_two-week-run-carries-weekend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5844 USD
---
## Findings
- **F1:** The 14-day run's power to predict the next day exists only from Friday's close, so the weekend effect is a Saturday effect. From Friday's close, the clipped 14-day run times the next day's unusual move has a mean of 0.0057 (t 2.94, 363 days, corr 0.142). From every other weekday's close |t| ≤ 1.25, and from Saturday's close it is −0.20. Friday's quintiles of the run order Saturday's unusual move from −0.37 % to +1.03 %.
- **F2:** The book's gain sits entirely on Saturday, while Sunday adds risk and no return. The book earns a mean 0.27 % on Saturdays and 0.008 % on Sundays, but Sunday's daily standard deviation is 1.52 %. 20 of the book's 30 worst days are Sundays, against 18 of its 30 best on Saturdays. This fits a Calmar of 0.454 that failed while the Sharpe was 0.70.
- **F3:** Thursday's close predicts the next two days (Friday and Saturday) at least as well as Friday's close predicts the weekend. Thursday's 14-day run times the 2-day unusual move has a mean of 0.0084 (t 2.97, corr 0.134), against 0.0061 (t 2.79) from Friday. Thursday's 7-, 14- and 28-day runs all give t of 2.67 to 2.97, while Friday's 3- and 7-day runs give only 0.88 and 1.70.
- **F4:** In each coin's top third of 20-day volatility, a down day is followed by a rebound the next day, graded by the size of the fall. Down days are followed by a mean next-day unusual move of +0.68 % (t 3.05, 1008 days). By quartile of the fall, the most extreme (−1.57 usual moves) is followed by +1.57 % (t 2.99), the next by +0.62 % (t 1.96) and the mildest two by +0.10 % and +0.41 %. In the low-volatility third, one-day reversal is absent (t −1.36). Across all volatility, the high-volatility reversal gives t 3.61.
- **F5:** The high-volatility reversal holds on its own in most coins and years, though not in 2025. BTC, ETH, XMR and ZEC each give t of 2.99 to 3.52; LTC gives 1.53 and XRP 1.10. Seven of eight years are positive, and 2025 is −0.0008 (t −0.18).
- **F6:** The brief's own angle shows nothing at a 5-day horizon. The position in the 60-day range runs from the bottom quintile at −0.51 % to the top at +0.83 % over 5 days, but no quintile has |t| above 1.05. Some 50 angles were looked at, so only the t values near 3 above are taken as findings.

## Ideas
- `031-01.g1.g1.g1.g1_two-week-run-carries-saturday` (from F1, F2): The higher a coin's 14-day return, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday alone.
- `031-01.g1.g1.g1.g2_thursday-run-carries-two-days` (from F3, F1): The higher a coin's 14-day return, measured in its usual daily moves at Thursday's close (UTC), the more it rises over the following Friday and Saturday together.
- `031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound` (from F4, F5): When a coin's last 20 days have been unusually volatile for it, the larger its one-day fall measured in its usual daily moves, the more it rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
