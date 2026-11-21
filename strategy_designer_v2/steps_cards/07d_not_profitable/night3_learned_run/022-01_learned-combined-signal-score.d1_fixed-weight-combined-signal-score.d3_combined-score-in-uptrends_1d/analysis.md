---
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3511 USD
---
## Findings
- **F1:** The book's loss comes almost entirely from its short positions in the "trending" regime. There they lost 25.0 bps per bar over 4745 bars, against +3.4 bps per bar for its 3343 long bars. Outside that regime, shorts lost 2.4 bps over 1442 bars and longs gained 2.8 bps over 1587 bars.
- **F2:** The shorts lost in 7 of the 8 years: -13 to -39 bps per bar in 2019-2021 and 2023-2025, and +4.8 in 2018 and +30.1 in 2022. The longs lost only in 2018 (-16.0) and 2023 (-8.4) and gained up to +11.8 bps in 2024. So the failure holds in almost every period, which matches the failed leave-one-window-out Sharpe of -1.24.
- **F3:** Inside the gate (28-day return up), the learned score was short on 57 % of bars. Its rank correlation is -0.24 with nearness to the 90-day high and -0.19 with negative 30-day volatility, but only +0.09 with 28-day momentum. In a rising month, the learned weights therefore bet against coins near their highs and against calm coins.
- **F4:** Those bets point the wrong way. On non-overlapping 5-day cases in the gate, the score's short cases had an excess return of +0.78 % (t 2.03, 961 cases) and its long cases -0.40 % (t -0.91, 701 cases). The slope on the score was negative (t -1.15, 1662 cases), so the learned combination does not carry forward to unseen dates.
- **F5:** The size per case is -0.74 % in total and -0.65 % unusual, against a 0.19 % round trip: -3.8 and -3.4 times the cost. No holding period or sizing can turn this into a gain. The cause is the sign of the bets, not the cost.
- **F6:** In the gate, the coin itself rose over the next 5 days, more so in the upper half of its 28-day rise. By quartile of the 28-day return (lowest to highest), the total 5-day move was +0.61 % (t 1.19), -0.16 %, +1.89 % (t 2.78) and +1.49 % (t 2.20), with 320 to 325 cases each. The upper two quartiles' moves are about 8 to 10 times a 0.19 % round trip.
- **F7:** Over all bars, the top fifth of the 28-day return was followed by a +1.11 % excess 5-day return (t 1.98, 490 cases). The 28-day return's correlation with the next 5-day excess return was +0.041 (t 2.01, 2450 cases). Of the four signals, only momentum carries a positive and roughly consistent effect.
- **F8:** While the 28-day return is down, distance below the 90-day high predicts the next 5 days: correlation -0.094, t -2.58, 751 cases. The further a falling coin is below its 90-day high, the higher its next 5-day return.

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends.d1_momentum-led-score-in-uptrends` (from F1, F3, F4, F6, F7): When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is, only while its 28-day return is up, and there the rise is larger the stronger the score, with the 28-day return carrying most of the score's weight in place of nearness to the 90-day high and low 30-day volatility.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends.d2_uptrend-strength-predicts-continuation` (from F1, F2, F6, F7): While a coin's 28-day return is up, its return over the next 5 days is higher the larger that 28-day rise.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends.d3_deep-drawdown-rebound-in-downtrends` (from F8, F5): While a coin's 28-day return is down, its return over the next 5 days is higher the further its close lies below its 90-day high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
