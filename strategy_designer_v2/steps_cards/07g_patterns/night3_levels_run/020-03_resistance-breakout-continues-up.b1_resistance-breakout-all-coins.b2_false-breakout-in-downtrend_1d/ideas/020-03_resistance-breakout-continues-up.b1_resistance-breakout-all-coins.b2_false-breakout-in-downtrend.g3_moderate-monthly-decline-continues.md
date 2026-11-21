---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the past 30 days, up to a moderate decline measured against its volatility, the more it falls over the next 10 days, whether or not it has just crossed a past turning price.
Consequence: A moderately falling month, rather than a break of a past level inside it, is the reason to refuse a long.
Why:
- F1: The coin's 30-day return predicts the next 10 days in its own direction, except at the extreme low end. Per coin, by 30-day return quintile, the drift-adjusted next-10-day move on non-overlapping grid bars is −0.96 % (t −0.87, n 530), −2.13 % (t −3.87, n 524), −1.35 % (t −1.93, n 522), +0.61 % (t 1.10, n 524) and +3.18 % (t 3.19, n 528). By decile, the lowest one is flat (+0.05 %, t 0.53, n 268), and deciles 1 to 3 fall by about 2 % each (t −1.9 to −2.8).
- F5: The resistance break adds nothing inside a falling month, so the tested idea's edge comes from the regime, not from the break. On grid bars with a negative 30-day return, the next 10 days are −1.32 % with a fresh break (n 166) and −1.38 % without one (n 1147). Across break cases, the quartiles of the break's strength show no grading (−1.86, −0.28, −2.42, −2.26 %).
- F6: The book loses because it shorts a coin whose own drift is up, which costs more than the timing earns. All 2229 trades are shorts, with a mean net of −3.49 % and 34 % winners. The book earns only in the years the coins fell: 2018 +7.1 bps a day against coins at −34.9, 2022 +5.2 against −24.7, and 2025 +5.8 against −2.6. It loses in rising years, for example 2023 −15.0 bps a day against coins at +31.7.
