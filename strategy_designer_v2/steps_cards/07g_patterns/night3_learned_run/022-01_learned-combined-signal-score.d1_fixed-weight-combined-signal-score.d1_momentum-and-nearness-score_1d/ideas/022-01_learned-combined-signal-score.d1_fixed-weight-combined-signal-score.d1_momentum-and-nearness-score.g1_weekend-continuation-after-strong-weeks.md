---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a Friday or a Saturday, a coin's return over the next 1 day is higher the larger its 7-day return was, measured against its 20-day volatility.
Consequence: A trader would lean further long into the weekend the stronger the coin's past week has been, and decline weekend longs after a weak week.
Why:
- F3: On Fridays and Saturdays, a coin's next-day unusual return rises with its prior 7-day return in units of its 20-day volatility. The slope's t is 5.63 on 4554 days, against t 1.56 on the other 11386 days. The top fifth of prior weeks was followed by +0.94 % (t 5.38), the bottom fifth by +0.18 % (t 1.14).
- F4: The Friday/Saturday grading holds on 5 of 6 coins and in 5 of 8 years. By coin, t ranges 1.91 to 4.06, except XMR at −0.09. By year, t is 2.0 to 3.6 in 2020 to 2024, and about 0 in 2018, 2019 and 2025.
- F5: Saturdays rise more than other days, by +0.39 % per day (Welch t 4.26). Saturday's mean is positive in 66 % of 144 coin-windows and on all 6 coins (t 1.40 to 2.92).
- F8: Both one-day moves are large next to cost, but they cover one day, not 5. The +0.94 % weekend move and the +0.60 % rebound are 4.9 and 3.2 times the backtest's 0.19 % round trip. Across up to ~30 angles examined, F3 and F5 stand out most clearly; F6 is weaker.
