---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The louder a coin's average four-hour high-to-low range over the past 7 days is compared with its average over the past 30 days, the higher its return over the next three days.
Consequence: A trader should favour long exposure to a coin whose recent week has been unusually turbulent and stay away from one whose week has been unusually quiet, rather than waiting for a quiet range to break.
Why:
- F1: The coin's own volatility ratio predicts its next 3 days, and in the opposite direction to the tested idea: the louder a coin's average 4-hour range over the past 7 days was against its 30-day average, the higher its 18-bar return. Per-coin quintiles step up steadily from an unusual move of −0.82 % in the quietest fifth to −0.39 %, −0.19 %, +0.21 % and +1.00 % in the loudest. Loudest minus quietest is t 5.2 (Spearman 0.056, p 8e-8, 9,046 non-overlapping cases). The 1.8-point gap is about 8 times a 0.22 % round trip.
- F2: The volatility-ratio effect has the same sign in most coins but not in every year. Loudest minus quietest is positive in 17 of 19 coins (t up to 2.7 on XRP, 2.2 on UNI, 2.0 on DOGE). By year it is positive in 2020, 2021 (t 2.8), 2023 and 2024 (t 8.4), near zero in 2022 and 2025, and negative in 2018 (t −1.7) and 2019. Its loudest-fifth median is −0.14 % against a mean of +1.00 %, so a minority of large rises carries it.
- F3: Quiet weeks that fell are followed by below-normal returns, and loud weeks that rose by above-normal ones. Quiet (lower two thirds of the volatility ratio) with a negative 7-day return gives a mean strength of −0.089 (t −5.5, 3,017 cases). Loud with a positive 7-day return gives +0.105 (t 3.5, 1,592 cases). Inside each cell the grading by the ratio is weak (rho −0.02 to 0.05).
- F5: The tested forecast does not grade the 3-day move: its Spearman with the next 18-bar strength is −0.0003 (12,086 cases). The book's position is also nearly flat across volatility-ratio quintiles (mean allocation 0.44 to 0.55), so the book does not use F1.
