---
line: 7.g patterns
backtest: 032-03.b2.b1_deep-calm-decline-more-coins_1d
idea tested: 032-03.b2.b1_deep-calm-decline-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4327 USD
---
## Findings
- **F1:** On thin-volume bars (the strategy's mean_reversion regime), the 28-day return carries forward in both directions: on the 10-day grid, the excess 10-day return rises steadily across the coin's 28-day-return quintiles, from -7.25 % (t -3.37, 84 cases on 33 days) through -2.29 %, +1.27 % and +5.88 % to +6.01 % (t 2.08, 60 cases on 26 days); outside that regime the quintiles show no order (-1.9 %, -3.6 %, +2.4 %, -0.0 %, +0.2 %, every t under 1.8 in size).
- **F2:** Scaled by the coin's 20-day volatility, the 28-day return predicts the excess return on thin-volume bars at every horizon: slope t 2.02 over 5 days (1016 cases, 190 days), 2.51 over 10 days (489 cases, 93 days) and 2.08 over 20 days (215 cases, 40 days); on the other bars it predicts nothing (t 0.26, 0.18, -0.09).
- **F3:** This continuation is not stable across periods: the 10-day slope on thin-volume bars is positive in 5 of 11 windows and negative in 6 (w14 -0.18, t -5.4); by year it is positive in 2019 to 2021 (t 1.25, 0.92, 1.23) and negative in 2018 (t -0.84); split by side, it is t 1.63 on falling coins (261 cases) and t 0.82 on rising coins (228 cases).
- **F4:** The deepest-forecast bars do fall: the excess 10-day return is -4.5 % (t -3.1, 90 cases) for forecasts below -10 and -3.5 % (t -2.4, 102) for forecasts from -10 to -5. The book still loses because short trades opened on weak forecasts lose heavily: -8.1 % net per trade for entry forecasts from -5 to -2 (t -4.0, 190 trades) and -3.7 % from -10 to -5 (t -3.8, 428 trades), against -0.5 % below -10 (t -0.9, 546 trades).
- **F5:** The losing trades are the short ones: trades held up to 10.5 days lose -4.6 % on average (603 trades) and those of 10.5 to 15 days lose -9.1 % (152). Trades held 25 to 50 days gain +2.7 % (180, median +8.4 %) and those over 50 days gain +2.9 % (83, median +12.0 %).
- **F6:** Other angles were looked at and none stands out once the number of angles is counted: the next 3 days after the strongest 7-day rises show +1.7 % (t 2.66), but the order across quintiles is broken (the second quintile is -1.1 %, t -3.3); Monday gives -0.38 % (t -2.7) and Friday +0.38 % (t 2.8) a day, with no theory behind them; widest-range days give +1.3 % over 3 days (t 2.06); large daily moves and volatility terciles show nothing with t above 2.

## Ideas
- `032-03.b2.b1.g1_calm-trend-continues-both-ways` (from F1, F2, F3): For a coin whose volume over the past 28 days is below its usual volume, its 28-day return, measured against its own daily volatility, continues over the next 10 days: the larger that volatility-scaled return in either direction, the larger the move the same way over the following 10 days.
- `032-03.b2.b1.g2_calm-decline-longer-horizon` (from F2, F4, F5): For a coin whose volume over the past 28 days is below its usual volume, the larger its 28-day fall, measured against its own daily volatility, the larger its further fall over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
