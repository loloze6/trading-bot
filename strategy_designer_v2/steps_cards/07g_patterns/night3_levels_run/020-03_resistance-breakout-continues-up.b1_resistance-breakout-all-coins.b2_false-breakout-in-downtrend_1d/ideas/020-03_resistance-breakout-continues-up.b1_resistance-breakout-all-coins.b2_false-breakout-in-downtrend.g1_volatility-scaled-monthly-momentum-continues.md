---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin has risen over the past 30 days relative to its own 30-day volatility, the more it rises over the next 10 days.
Consequence: A strong, steady 30-day rise is a reason to hold or buy a coin for the next 10 days rather than fade it.
Why:
- F1: The coin's 30-day return predicts the next 10 days in its own direction, except at the extreme low end. Per coin, by 30-day return quintile, the drift-adjusted next-10-day move on non-overlapping grid bars is −0.96 % (t −0.87, n 530), −2.13 % (t −3.87, n 524), −1.35 % (t −1.93, n 522), +0.61 % (t 1.10, n 524) and +3.18 % (t 3.19, n 528). By decile, the lowest one is flat (+0.05 %, t 0.53, n 268), and deciles 1 to 3 fall by about 2 % each (t −1.9 to −2.8).
- F2: Scaling the 30-day return by the coin's 30-day volatility sharpens the top end. Its highest quintile is followed by +3.53 % drift-adjusted over 10 days (strength 0.19, t 3.66, n 528). That is about 16 times the 0.22 % cost of a round trip.
- F3: The rise after the strongest 30-day returns holds across coins but not in bear years. In the top two deciles, 16 of 19 coins have a positive mean. By year it is positive in 2020 (+3.1 %, t 1.8), 2021 (+11.2 %, t 2.9), 2023 (+3.6 %, t 2.1) and 2024 (+3.6 %, t 2.3). It is negative in 2018 (−17.7 %, n 7) and 2022 (−4.9 %, t −2.0).
